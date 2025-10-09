"""
Vercel serverless function entry point for Flask application.
This file is the entry point for Vercel's Python runtime.
"""
import os
import sys
import traceback

# Add the parent directory to the path so we can import from src
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

print(f"[Vercel Init] Python version: {sys.version}")
print(f"[Vercel Init] Current directory: {current_dir}")
print(f"[Vercel Init] Parent directory: {parent_dir}")
print(f"[Vercel Init] sys.path: {sys.path[:3]}")

try:
    print("[Vercel Init] Attempting to import Flask app from src.main...")
    from src.main import app
    print("[Vercel Init] ✓ Flask app imported successfully!")
    
    # Vercel will call this handler
    # The app is already configured in src/main.py
    handler = app
    print("[Vercel Init] ✓ Handler configured!")
    
except Exception as e:
    print(f"[Vercel Init] ✗ Error during initialization: {e}")
    print(f"[Vercel Init] Traceback:")
    traceback.print_exc()
    
    # Create a minimal error handler
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
    @app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
    def error_handler(path=None):
        return jsonify({
            'error': 'Application failed to initialize',
            'message': str(e),
            'type': type(e).__name__,
            'help': 'Check Vercel function logs for details'
        }), 500
    
    handler = app
    print("[Vercel Init] ✓ Error handler configured")
