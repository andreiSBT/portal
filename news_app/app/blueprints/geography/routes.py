from flask import render_template
from flask_login import login_required
from app.blueprints.geography import geography_bp


@geography_bp.route('/')
@login_required
def index():
    """Geography & History main page"""
    return render_template('geography/index.html')


@geography_bp.route('/maps')
@login_required
def maps():
    """Maps and Territories page"""
    return render_template('geography/maps.html')


@geography_bp.route('/timeline')
@login_required
def timeline():
    """Historical Timeline page"""
    return render_template('geography/timeline.html')


@geography_bp.route('/symbols')
@login_required
def symbols():
    """National Symbols page"""
    return render_template('geography/symbols.html')
