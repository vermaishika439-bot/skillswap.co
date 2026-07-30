"""
profile_routes.py
-------------------
Public user profile pages, plus the logged-in user's own
settings page (edit profile, change password, dark mode, delete account).
"""

import os
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, session, flash, current_app
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models.db import get_db
from routes.helpers import login_required

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile/<int:user_id>")
def view_profile(user_id):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()

    if user is None:
        flash("That user doesn't exist.", "error")
        return redirect(url_for("main.browse_skills"))

    skills_offered = db.execute(
        "SELECT * FROM skills_offered WHERE user_id = ?", (user_id,)
    ).fetchall()
    skills_wanted = db.execute(
        "SELECT * FROM skills_wanted WHERE user_id = ?", (user_id,)
    ).fetchall()

    ratings = db.execute(
        """SELECT r.*, u.name as rater_name FROM ratings r
           JOIN users u ON u.id = r.rater_user_id
           WHERE r.rated_user_id = ? ORDER BY r.created_at DESC""",
        (user_id,)
    ).fetchall()

    avg_rating_row = db.execute(
        "SELECT AVG(stars) as avg_r, COUNT(*) as total FROM ratings WHERE rated_user_id = ?",
        (user_id,)
    ).fetchone()
    avg_rating = round(avg_rating_row["avg_r"], 1) if avg_rating_row["avg_r"] else 0

    is_own_profile = session.get("user_id") == user_id

    return render_template(
        "profile.html",
        profile_user=user,
        skills_offered=skills_offered,
        skills_wanted=skills_wanted,
        ratings=ratings,
        avg_rating=avg_rating,
        avg_rating_total=avg_rating_row["total"],
        is_own_profile=is_own_profile,
    )


@profile_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    db = get_db()
    user_id = session["user_id"]

    if request.method == "POST":
        form_type = request.form.get("form_type")

        # --- Edit profile info ---
        if form_type == "edit_profile":
            name = request.form.get("name", "").strip()
            bio = request.form.get("bio", "").strip()
            location = request.form.get("location", "").strip()

            file = request.files.get("profile_image")
            if file and file.filename:
                ext = file.filename.rsplit(".", 1)[-1].lower()
                if ext in current_app.config["ALLOWED_EXTENSIONS"]:
                    filename = secure_filename(f"user{user_id}_{file.filename}")
                    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
                    file.save(filepath)
                    db.execute("UPDATE users SET profile_image = ? WHERE id = ?", (filename, user_id))

            db.execute(
                "UPDATE users SET name = ?, bio = ?, location = ? WHERE id = ?",
                (name, bio, location, user_id)
            )
            db.commit()
            session["user_name"] = name
            flash("Profile updated successfully.", "success")

        # --- Change password ---
        elif form_type == "change_password":
            current_password = request.form.get("current_password", "")
            new_password = request.form.get("new_password", "")

            user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            if not check_password_hash(user["password_hash"], current_password):
                flash("Current password is incorrect.", "error")
            else:
                new_hash = generate_password_hash(new_password)
                db.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_hash, user_id))
                db.commit()
                flash("Password updated successfully.", "success")

        # --- Toggle dark mode preference (also handled client-side via JS/localStorage) ---
        elif form_type == "toggle_dark_mode":
            new_value = 1 if request.form.get("dark_mode") == "on" else 0
            db.execute("UPDATE users SET dark_mode = ? WHERE id = ?", (new_value, user_id))
            db.commit()

        # --- Delete account ---
        elif form_type == "delete_account":
            db.execute("DELETE FROM users WHERE id = ?", (user_id,))
            db.commit()
            session.clear()
            flash("Your account has been deleted.", "info")
            return redirect(url_for("main.landing"))

        return redirect(url_for("profile.settings"))

    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    return render_template("settings.html", user=user)
