"""
Vercel serverless function entry point for Flask application.
This file is the entry point for Vercel's Python runtime.
"""
import os
import sys
import traceback

print("=" * 80)
print("[Vercel] Starting initialization...")
print("=" * 80)

# Add the parent directory to the path so we can import from src
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

print(f"[Vercel] Python: {sys.version}")
print(f"[Vercel] Current dir: {current_dir}")
print(f"[Vercel] Parent dir: {parent_dir}")

sys.path.insert(0, parent_dir)

# Import Flask app
print("[Vercel] Importing src.main...")
try:
    from src.main import app
    print("[Vercel] ✓ src.main imported successfully!")
    print(f"[Vercel] ✓ app type: {type(app)}")
except Exception as import_error:
    print(f"[Vercel] ✗ Import failed: {import_error}")
    traceback.print_exc()
    
    # Create minimal fallback
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/<path:path>', defaults={'path': ''})
    @app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
    def fallback(path=''):
        return jsonify({
            'error': 'Application import failed',
            'message': str(import_error),
            'type': type(import_error).__name__
        }), 500

print("=" * 80)
print("[Vercel] Initialization complete!")
print("=" * 80)
