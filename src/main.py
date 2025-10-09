import os
import sys
from dotenv import load_dotenv
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Load environment variables from repository root .env if present
repo_root = os.path.dirname(os.path.dirname(__file__))
env_path = os.path.join(repo_root, '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from pymongo import MongoClient

# Initialize Flask
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app)

# Configure MongoDB connection via environment variable MONGO_URI or MONGODB_URI
# Example MONGO_URI: mongodb+srv://user:pass@cluster0.mongodb.net/mydb?retryWrites=true&w=majority
MONGO_URI = os.environ.get('MONGODB_URI') or os.environ.get('MONGO_URI')
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME', 'notetaker_db')

# Validate MongoDB URI is configured
if not MONGO_URI:
    print("⚠ WARNING: MongoDB connection string not configured.")
    print("   Set MONGODB_URI environment variable for database access.")
    print("   API will fail until this is configured.")
    # Don't raise error immediately - let the app start but fail on actual DB operations
    # This allows Vercel to show a better error message
    db = None
else:
    try:
        print(f"[MongoDB] Connecting to database '{MONGO_DB_NAME}'...")
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        # Test the connection
        client.admin.command('ping')
        db = client[MONGO_DB_NAME]
        print(f"✓ Successfully connected to MongoDB: {MONGO_DB_NAME}")
    except Exception as e:
        print(f"✗ Failed to connect to MongoDB: {e}")
        print(f"   URI (masked): {MONGO_URI[:30]}...{MONGO_URI[-20:]}")
        # Don't raise - let the app start but operations will fail
        db = None

# Make the db available to routes via app.config
app.config['MONGO_DB'] = db

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify service status"""
    status = {
        'status': 'ok',
        'service': 'NoteTaker API',
        'database': 'connected' if db is not None else 'disconnected'
    }
    if db is None:
        status['status'] = 'degraded'
        status['message'] = 'Database not connected - check MONGODB_URI environment variable'
        return jsonify(status), 503
    return jsonify(status), 200

# register blueprints (import after db is configured to avoid circular imports)
from src.routes.user import user_bp
from src.routes.note import note_bp

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(note_bp, url_prefix='/api')

# Only serve static files when running locally (not on Vercel)
# On Vercel, static files are served from public/ directory
if not os.environ.get('VERCEL'):
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        static_folder_path = app.static_folder
        if static_folder_path is None:
            return "Static folder not configured", 404

        if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
            return send_from_directory(static_folder_path, path)
        else:
            index_path = os.path.join(static_folder_path, 'index.html')
            if os.path.exists(index_path):
                return send_from_directory(static_folder_path, 'index.html')
            else:
                return "index.html not found", 404


if __name__ == '__main__':
    # Determine debug flag from environment, but avoid enabling the interactive
    # debugger or the reloader on Windows where they can trigger
    # OSError: [WinError 10038] "operation on non-socket".
    env_debug = os.environ.get('FLASK_DEBUG', '')
    debug_mode = env_debug.lower() in ('1', 'true', 'yes')

    # On Windows, prefer running without the debugger/reloader to avoid
    # selector/socket issues in the development server.
    use_reloader = False
    if os.name == 'nt':
        debug_mode = False

    try:
        app.run(host='0.0.0.0', port=5001, debug=debug_mode, use_reloader=use_reloader)
    except OSError as e:
        # Provide a clearer message for the specific Windows error we sometimes hit
        winerr = getattr(e, 'winerror', None)
        if winerr == 10038:
            print("OSError: WinError 10038 encountered. This typically happens on Windows when the Flask/Werkzeug reloader or debugger interacts with sockets.")
            print("Workarounds: run with FLASK_DEBUG=0 (or unset), make sure use_reloader=False, or use a production WSGI server (Waitress/gunicorn).")
            sys.exit(1)
        raise
