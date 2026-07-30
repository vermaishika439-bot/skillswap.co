"""
helpers.py
-----------
Small shared utilities used across multiple route blueprints.
Keeping this separate avoids circular imports between blueprint files.
"""

from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(view_func):
    """
    Decorator that blocks access to a route unless the user is logged in.
    Usage:
        @dashboard_bp.route("/dashboard")
        @login_required
        def dashboard():
            ...
    """
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "error")
            return redirect(url_for("auth.login"))
        return view_func(*args, **kwargs)
    return wrapped
