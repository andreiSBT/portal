import os
from app import create_app
from app.extensions import db
from app.models import User, NewsCategory, NewsArticle

app = create_app(os.getenv('FLASK_ENV') or 'default')


@app.shell_context_processor
def make_shell_context():
    """Make database models available in Flask shell"""
    return {
        'db': db,
        'User': User,
        'NewsCategory': NewsCategory,
        'NewsArticle': NewsArticle
    }


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
