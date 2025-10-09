"""
Vercel serverless function entry point for Flask application.
This file is the entry point for Vercel's Python runtime.
"""
import os
import sys

# Add the parent directory to the path so we can import from src
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.main import app

# Vercel will call this handler
# The app is already configured in src/main.py
handler = app
