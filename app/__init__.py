from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'


def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)

    # User loader for Flask-Login
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints/routes
    from app import routes, models
    from app.auth import bp as auth_bp
    app.register_blueprint(routes.bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Create database tables (needed for Vercel serverless)
    # Only create tables if we have a proper database URL (not SQLite on Vercel)
    try:
        with app.app_context():
            db.create_all()
    except Exception as e:
        app.logger.warning(f"Could not create database tables: {e}")

    return app
