import os
import sys

# Add the parent directory to the path so we can import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from run import app

# Export the Flask app for Vercel
# Vercel will use this as the WSGI application
# Fiascha Portal App
app = app
