"""
dashboard_routes.py
---------------------
The logged-in user's home base: welcome banner, stats cards,
recent swap requests, their own skills, and notifications.
"""

from flask import Blueprint, render_template, session
from models.db import get_db
from routes.helpers import login_required

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    db = get_db()
    user_id = session["user_id"]

    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()

    skills_offered = db.execute(
        "SELECT * FROM skills_offered WHERE user_id = ?", (user_id,)
    ).fetchall()
    skills_wanted = db.execute(
        "SELECT * FROM skills_wanted WHERE user_id = ?", (user_id,)
    ).fetchall()

    # Recent swap requests involving this user (either sent or received)
    recent_requests = db.execute(
        """SELECT sr.*, 
                  su.name as sender_name, su.profile_image as sender_image,
                  ru.name as receiver_name, ru.profile_image as receiver_image
           FROM swap_requests sr
           JOIN users su ON su.id = sr.sender_id
           JOIN users ru ON ru.id = sr.receiver_id
           WHERE sr.sender_id = ? OR sr.receiver_id = ?
           ORDER BY sr.created_at DESC
           LIMIT 5""",
        (user_id, user_id)
    ).fetchall()

    # --- Stats cards ---
    pending_count = db.execute(
        "SELECT COUNT(*) as c FROM swap_requests WHERE receiver_id = ? AND status = 'pending'",
        (user_id,)
    ).fetchone()["c"]

    accepted_count = db.execute(
        """SELECT COUNT(*) as c FROM swap_requests 
           WHERE (sender_id = ? OR receiver_id = ?) AND status = 'accepted'""",
        (user_id, user_id)
    ).fetchone()["c"]

    unread_messages = db.execute(
        "SELECT COUNT(*) as c FROM messages WHERE receiver_id = ? AND is_read = 0",
        (user_id,)
    ).fetchone()["c"]

    avg_rating_row = db.execute(
        "SELECT AVG(stars) as avg_r, COUNT(*) as total FROM ratings WHERE rated_user_id = ?",
        (user_id,)
    ).fetchone()
    avg_rating = round(avg_rating_row["avg_r"], 1) if avg_rating_row["avg_r"] else 0

    return render_template(
        "dashboard.html",
        user=user,
        skills_offered=skills_offered,
        skills_wanted=skills_wanted,
        recent_requests=recent_requests,
        pending_count=pending_count,
        accepted_count=accepted_count,
        unread_messages=unread_messages,
        avg_rating=avg_rating,
        avg_rating_total=avg_rating_row["total"],
    )
