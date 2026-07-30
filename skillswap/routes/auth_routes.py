"""
auth_routes.py
---------------
Handles user authentication: signup, login, logout.
Passwords are never stored in plain text — we use Werkzeug's
generate_password_hash / check_password_hash helpers.
"""

import os
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, session, flash, current_app
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models.db import get_db

auth_bp = Blueprint("auth", __name__)


def allowed_file(filename):
    """Checks that an uploaded file has an allowed image extension."""
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        db = get_db()

        # --- Collect form fields ---
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        bio = request.form.get("bio", "").strip()
        location = request.form.get("location", "").strip()
        skills_teach = request.form.get("skills_teach", "")
        skills_learn = request.form.get("skills_learn", "")

        # --- Basic validation ---
        if not name or not email or not password:
            flash("Name, email, and password are required.", "error")
            return redirect(url_for("auth.signup"))

        existing = db.execute(
            "SELECT id FROM users WHERE email = ?", (email,)
        ).fetchone()
        if existing:
            flash("An account with that email already exists.", "error")
            return redirect(url_for("auth.signup"))

        # --- Handle profile picture upload (optional) ---
        profile_image = "default-avatar.png"
        file = request.files.get("profile_image")
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Prefix with a placeholder-safe unique name to avoid collisions
            unique_name = f"{email.split('@')[0]}_{filename}"
            filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], unique_name)
            file.save(filepath)
            profile_image = unique_name

        # --- Save user to database ---
        password_hash = generate_password_hash(password)
        cursor = db.execute(
            """INSERT INTO users (name, email, password_hash, bio, location, profile_image)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (name, email, password_hash, bio, location, profile_image)
        )
        user_id = cursor.lastrowid

        # --- Save skills (comma-separated input -> individual rows) ---
        for skill in [s.strip() for s in skills_teach.split(",") if s.strip()]:
            db.execute(
                "INSERT INTO skills_offered (user_id, skill_name) VALUES (?, ?)",
                (user_id, skill)
            )
        for skill in [s.strip() for s in skills_learn.split(",") if s.strip()]:
            db.execute(
                "INSERT INTO skills_wanted (user_id, skill_name) VALUES (?, ?)",
                (user_id, skill)
            )

        db.commit()

        # Log the user in immediately after signup
        session["user_id"] = user_id
        session["user_name"] = name
        flash(f"Welcome to SkillSwap, {name}! 🎉", "success")
        return redirect(url_for("dashboard.dashboard"))

    return render_template("signup.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        db = get_db()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        remember = request.form.get("remember")  # "on" if checked

        user = db.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()

        if user is None or not check_password_hash(user["password_hash"], password):
            flash("Invalid email or password.", "error")
            return redirect(url_for("auth.login"))

        # Successful login — create session
        session["user_id"] = user["id"]
        session["user_name"] = user["name"]

        # "Remember me" -> make session last 30 days instead of closing on browser exit
        session.permanent = True if remember else False

        flash(f"Welcome back, {user['name']}!", "success")
        return redirect(url_for("dashboard.dashboard"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You've been logged out.", "info")
    return redirect(url_for("main.landing"))
