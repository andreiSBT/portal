import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

def get_database_url():
    """Get database URL and fix postgres:// to postgresql:// for SQLAlchemy.

    In production, requires POSTGRES_URL (or DATABASE_URL / DATABASE_URI) to be set.
    To configure on Vercel:
      1. Vercel Dashboard -> Project -> Storage -> Create Database -> Postgres
         (Vercel auto-sets POSTGRES_URL once the database is linked)
      2. Or manually: Settings -> Environment Variables -> add POSTGRES_URL
    """
    url = os.environ.get('POSTGRES_URL') or \
          os.environ.get('DATABASE_URL') or \
          os.environ.get('DATABASE_URI')
    if url and url.startswith('postgres://'):
        url = url.replace('postgres://', 'postgresql://', 1)
    if url:
        return url
    # In production, SQLite won't work (e.g. Vercel has a read-only filesystem)
    if os.environ.get('FLASK_ENV') == 'production':
        raise RuntimeError(
            "No database URL configured. Set POSTGRES_URL in your environment. "
            "On Vercel: Dashboard -> Project -> Storage -> Create/Link a Postgres database, "
            "or add POSTGRES_URL under Settings -> Environment Variables."
        )
    return 'sqlite:///' + os.path.join(basedir, 'todo_dev.db')

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-please-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = get_database_url()
    SERVER_NAME = os.environ.get('SERVER_NAME')

class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = False  # Set to True to see SQL queries in console
    SERVER_NAME = None  # Disable SERVER_NAME in development for flexibility

class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = get_database_url()
    # Remove SERVER_NAME for Vercel - it handles routing automatically

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
