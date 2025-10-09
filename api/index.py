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
print(f"[Vercel] CWD: {os.getcwd()}")

# Check if parent directory exists and has src folder
print(f"[Vercel] Parent dir exists: {os.path.exists(parent_dir)}")
src_dir = os.path.join(parent_dir, 'src')
print(f"[Vercel] src dir: {src_dir}")
print(f"[Vercel] src dir exists: {os.path.exists(src_dir)}")

if os.path.exists(src_dir):
    print(f"[Vercel] Files in src: {os.listdir(src_dir)[:10]}")

sys.path.insert(0, parent_dir)
print(f"[Vercel] sys.path[0]: {sys.path[0]}")

# Try to import step by step to see where it fails
print("[Vercel] Step 1: Importing os and sys - OK")

try:
    print("[Vercel] Step 2: Importing Flask...")
    from flask import Flask
    print("[Vercel] Step 2: Flask imported - OK")
except Exception as e:
    print(f"[Vercel] Step 2: FAILED - {e}")
    traceback.print_exc()
    raise

try:
    print("[Vercel] Step 3: Importing dotenv...")
    from dotenv import load_dotenv
    print("[Vercel] Step 3: dotenv imported - OK")
except Exception as e:
    print(f"[Vercel] Step 3: FAILED - {e}")
    traceback.print_exc()
    raise

try:
    print("[Vercel] Step 4: Importing pymongo...")
    from pymongo import MongoClient
    print("[Vercel] Step 4: pymongo imported - OK")
except Exception as e:
    print(f"[Vercel] Step 4: FAILED - {e}")
    traceback.print_exc()
    raise

try:
    print("[Vercel] Step 5: Importing src.main...")
    from src.main import app
    print("[Vercel] Step 5: src.main imported - OK")
    print("[Vercel] Step 5: app object:", type(app))
except Exception as e:
    print(f"[Vercel] Step 5: FAILED - {e}")
    print(f"[Vercel] Error type: {type(e).__name__}")
    print(f"[Vercel] Error details:")
    traceback.print_exc()
    
    # Create emergency fallback app
    print("[Vercel] Creating emergency fallback app...")
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
    @app.route('/', defaults={'path': ''})
    def emergency_handler(path=''):
        return jsonify({
            'error': 'Application failed to initialize',
            'message': str(e),
            'error_type': type(e).__name__,
            'step': 'importing src.main',
            'help': 'Check Vercel function logs for full traceback'
        }), 500

print("=" * 80)
print("[Vercel] Initialization complete!")
print("=" * 80)

# Export for Vercel - use the imported app directly
# Don't reassign, just ensure it's in module scope
