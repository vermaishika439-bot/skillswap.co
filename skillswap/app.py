"""
app.py
-------
Entry point for the SkillSwap Flask application.
Run with:  python app.py
Then visit http://127.0.0.1:5000 in your browser.
"""

from flask import Flask
from datetime import timedelta

from config import Config
from models.db import init_db

# Import all blueprints (one per feature area — see routes/ folder)
from routes.auth_routes import auth_bp
from routes.main_routes import main_bp
from routes.dashboard_routes import dashboard_bp
from routes.profile_routes import profile_bp
from routes.swap_routes import swap_bp
from routes.chat_routes import chat_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # "Remember me" sessions last 30 days; normal sessions end on browser close
    app.permanent_session_lifetime = timedelta(days=30)

    # Set up the SQLite database (creates tables on first run)
    init_db(app)

    # Register all blueprints so their routes become active
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(swap_bp)
    app.register_blueprint(chat_bp)

    return app


app = create_app()

if __name__ == "__main__":
    # debug=True gives auto-reload + detailed error pages during development
    app.run(debug=True)
