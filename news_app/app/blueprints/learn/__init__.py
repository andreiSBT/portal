from flask import Blueprint

learn_bp = Blueprint('learn', __name__)

from app.blueprints.learn import routes
