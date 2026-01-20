import os
import sys

# Add the parent directory to the path so we can import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from run import app

# Vercel serverless function handler
def handler(event, context):
    return app(event, context)

# For Vercel to use the Flask app
application = app
