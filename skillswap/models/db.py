"""
db.py
------
Handles all raw SQLite connection logic for the app.
We use Python's built-in sqlite3 module (no ORM) to keep things
simple and beginner-friendly, while still using safe parameterized
queries everywhere to prevent SQL injection.
"""

import sqlite3
import os
from flask import current_app, g

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")


def get_db():
    """
    Returns a database connection for the current request.
    Flask's 'g' object stores it so we only open ONE connection
    per request, no matter how many times get_db() is called.
    """
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        # This makes rows behave like dictionaries (row['name'] instead of row[0])
        g.db.row_factory = sqlite3.Row
        # Enforce foreign key constraints (off by default in SQLite)
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None):
    """Closes the database connection at the end of the request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app):
    """
    Creates all tables from schema.sql if the database file
    doesn't exist yet. Called once when the app starts.
    """
    db_exists = os.path.exists(app.config["DATABASE"])

    if not db_exists:
        with app.app_context():
            db = get_db()
            with open(SCHEMA_PATH, "r") as f:
                db.executescript(f.read())
            db.commit()
            print("✅ Database created and initialized with schema.sql")

    # Register close_db so it runs automatically after every request
    app.teardown_appcontext(close_db)
