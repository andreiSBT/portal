from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Register blueprints/routes
    from app import routes, models
    app.register_blueprint(routes.bp)

    # Create database tables (needed for Vercel serverless)
    # Only create tables if we have a proper database URL (not SQLite on Vercel)
    try:
        with app.app_context():
            db.create_all()
    except Exception as e:
        app.logger.warning(f"Could not create database tables: {e}")

    return app
