"""
chat_routes.py
----------------
A simple messaging system between two users. Not real-time
(no WebSockets, per project constraints) — messages load on
page request and can be polled/refreshed via JS if desired.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from models.db import get_db
from routes.helpers import login_required

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/chat")
@chat_bp.route("/chat/<int:with_user_id>")
@login_required
def chat(with_user_id=None):
    db = get_db()
    user_id = session["user_id"]

    # Build the sidebar list: everyone this user has exchanged messages with
    conversations = db.execute(
        """SELECT DISTINCT u.id, u.name, u.profile_image
           FROM users u
           WHERE u.id IN (
               SELECT sender_id FROM messages WHERE receiver_id = ?
               UNION
               SELECT receiver_id FROM messages WHERE sender_id = ?
           )""",
        (user_id, user_id)
    ).fetchall()

    active_messages = []
    active_user = None

    if with_user_id:
        active_user = db.execute("SELECT * FROM users WHERE id = ?", (with_user_id,)).fetchone()
        active_messages = db.execute(
            """SELECT * FROM messages
               WHERE (sender_id = ? AND receiver_id = ?)
                  OR (sender_id = ? AND receiver_id = ?)
               ORDER BY sent_at ASC""",
            (user_id, with_user_id, with_user_id, user_id)
        ).fetchall()
        # Mark incoming messages as read
        db.execute(
            "UPDATE messages SET is_read = 1 WHERE sender_id = ? AND receiver_id = ?",
            (with_user_id, user_id)
        )
        db.commit()

    return render_template(
        "chat.html",
        conversations=conversations,
        active_user=active_user,
        active_messages=active_messages,
    )


@chat_bp.route("/chat/send/<int:receiver_id>", methods=["POST"])
@login_required
def send_message(receiver_id):
    db = get_db()
    sender_id = session["user_id"]
    content = request.form.get("content", "").strip()

    if content:
        db.execute(
            "INSERT INTO messages (sender_id, receiver_id, content) VALUES (?, ?, ?)",
            (sender_id, receiver_id, content)
        )
        db.commit()

    return redirect(url_for("chat.chat", with_user_id=receiver_id))
