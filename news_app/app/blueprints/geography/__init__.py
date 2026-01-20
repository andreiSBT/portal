from flask import Blueprint

geography_bp = Blueprint('geography', __name__)

from app.blueprints.geography import routes
