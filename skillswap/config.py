"""
config.py
----------
Central place for all app configuration values.
Keeping these separate from app.py makes it easy to change
settings (like the secret key or database path) without
touching application logic.
"""

import os

# BASE_DIR = the root folder of the project (skillswap/)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Secret key is used by Flask to sign session cookies (login sessions, flash messages).
    # In a real production app this should come from an environment variable, not be hardcoded.
    SECRET_KEY = os.environ.get("SECRET_KEY", "skillswap-dev-secret-key-change-this")

    # Path to our SQLite database file
    DATABASE = os.path.join(BASE_DIR, "database.db")

    # Where uploaded profile pictures get saved
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads", "profile_pics")

    # Only allow these file types for profile picture uploads (basic security)
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

    # Limit uploads to 3MB to prevent abuse
    MAX_CONTENT_LENGTH = 3 * 1024 * 1024
