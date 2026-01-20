import os
from app import create_app
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create Flask application instance
app = create_app(os.getenv('FLASK_ENV') or 'default')

# Vercel requires the app to be exposed at the module level
# This allows Vercel's serverless functions to import and use it
application = app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
