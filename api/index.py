"""
Vercel serverless function entry point for Flask application.
"""
import os
import sys
import traceback

print("[Vercel] Starting...")

# Setup path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

print(f"[Vercel] Python {sys.version}")
print(f"[Vercel] Importing src.main...")

# Try to import the main app
app = None
import_error_msg = None
import_error_type = None

try:
    from src.main import app as main_app
    app = main_app
    print("[Vercel] ✓ Main app imported successfully")
except Exception as e:
    import_error_msg = str(e)
    import_error_type = type(e).__name__
    print(f"[Vercel] ✗ Import failed: {e}")
    traceback.print_exc()

# If import failed, create fallback app
if app is None:
    print("[Vercel] Creating fallback app...")
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/<path:path>')
    @app.route('/')
    def fallback(path=''):
        return jsonify({
            'error': 'Application import failed',
            'message': import_error_msg or 'Unknown error',
            'type': import_error_type or 'Unknown',
            'help': 'Check Vercel function logs for details'
        }), 503

print("[Vercel] Ready!")
