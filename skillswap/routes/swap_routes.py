"""
swap_routes.py
----------------
Handles the full lifecycle of a skill-swap request:
sending, viewing (incoming/outgoing/pending/accepted/rejected),
accepting, and rejecting.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.db import get_db
from routes.helpers import login_required

swap_bp = Blueprint("swap", __name__)


@swap_bp.route("/swap/send/<int:receiver_id>", methods=["POST"])
@login_required
def send_request(receiver_id):
    db = get_db()
    sender_id = session["user_id"]

    if sender_id == receiver_id:
        flash("You can't send a swap request to yourself.", "error")
        return redirect(url_for("profile.view_profile", user_id=receiver_id))

    offered_skill = request.form.get("offered_skill", "").strip()
    wanted_skill = request.form.get("wanted_skill", "").strip()
    message = request.form.get("message", "").strip()

    db.execute(
        """INSERT INTO swap_requests (sender_id, receiver_id, offered_skill, wanted_skill, message)
           VALUES (?, ?, ?, ?, ?)""",
        (sender_id, receiver_id, offered_skill, wanted_skill, message)
    )
    db.commit()

    flash("Swap request sent!", "success")
    return redirect(url_for("profile.view_profile", user_id=receiver_id))


@swap_bp.route("/swap-requests")
@login_required
def swap_requests():
    db = get_db()
    user_id = session["user_id"]

    # Incoming = requests sent TO me
    incoming = db.execute(
        """SELECT sr.*, u.name as other_name, u.profile_image as other_image
           FROM swap_requests sr JOIN users u ON u.id = sr.sender_id
           WHERE sr.receiver_id = ? ORDER BY sr.created_at DESC""",
        (user_id,)
    ).fetchall()

    # Outgoing = requests I sent
    outgoing = db.execute(
        """SELECT sr.*, u.name as other_name, u.profile_image as other_image
           FROM swap_requests sr JOIN users u ON u.id = sr.receiver_id
           WHERE sr.sender_id = ? ORDER BY sr.created_at DESC""",
        (user_id,)
    ).fetchall()

    pending = [r for r in incoming + outgoing if r["status"] == "pending"]
    accepted = [r for r in incoming + outgoing if r["status"] == "accepted"]
    rejected = [r for r in incoming + outgoing if r["status"] == "rejected"]

    return render_template(
        "swap_requests.html",
        incoming=incoming,
        outgoing=outgoing,
        pending=pending,
        accepted=accepted,
        rejected=rejected,
    )


@swap_bp.route("/swap/respond/<int:request_id>/<string:action>", methods=["POST"])
@login_required
def respond_request(request_id, action):
    db = get_db()
    user_id = session["user_id"]

    swap = db.execute("SELECT * FROM swap_requests WHERE id = ?", (request_id,)).fetchone()

    if swap is None or swap["receiver_id"] != user_id:
        flash("You can't modify that request.", "error")
        return redirect(url_for("swap.swap_requests"))

    if action not in ("accepted", "rejected"):
        flash("Invalid action.", "error")
        return redirect(url_for("swap.swap_requests"))

    db.execute("UPDATE swap_requests SET status = ? WHERE id = ?", (action, request_id))
    db.commit()

    flash(f"Request {action}.", "success")
    return redirect(url_for("swap.swap_requests"))
