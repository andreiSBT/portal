from flask import render_template
from flask_login import login_required
from app.blueprints.learn import learn_bp


@learn_bp.route('/')
@login_required
def index():
    """Learn section main page"""
    return render_template('learn/index.html')


@learn_bp.route('/languages')
@login_required
def languages():
    """Languages and Culture page"""
    return render_template('learn/languages.html')


@learn_bp.route('/citizenship')
@login_required
def citizenship():
    """Citizenship Guide page"""
    return render_template('learn/citizenship.html')
