from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def admin_required(f):
    """Decorator to require admin access for a route"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        if not current_user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


def journalist_required(f):
    """Decorator to require journalist or admin access for a route"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))

        # Allow admins and journalists
        allowed_ranks = ['Journalist', 'Minister', 'President']
        if not (current_user.is_admin or current_user.citizen_rank in allowed_ranks):
            flash('Only journalists and officials can write articles.', 'danger')
            return redirect(url_for('main.welcome'))
        return f(*args, **kwargs)
    return decorated_function
