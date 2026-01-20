import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-please-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Support both DATABASE_URL (Vercel Postgres) and DATABASE_URI
    SQLALCHEMY_DATABASE_URI = os.environ.get('POSTGRES_URL') or \
        os.environ.get('DATABASE_URL') or \
        os.environ.get('DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'todo_dev.db')
    SERVER_NAME = os.environ.get('SERVER_NAME')

class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = False  # Set to True to see SQL queries in console
    SERVER_NAME = None  # Disable SERVER_NAME in development for flexibility

class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    # Use Vercel Postgres URL (POSTGRES_URL is automatically set by Vercel)
    SQLALCHEMY_DATABASE_URI = os.environ.get('POSTGRES_URL') or \
        os.environ.get('DATABASE_URL') or \
        os.environ.get('DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'todo.db')
    # Remove SERVER_NAME for Vercel - it handles routing automatically
    # Vercel will route based on your custom domain configuration

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
