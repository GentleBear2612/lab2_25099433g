import os
import sys
import time
from dotenv import load_dotenv
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Load environment variables from repository root .env if present
repo_root = os.path.dirname(os.path.dirname(__file__))
env_path = os.path.join(repo_root, '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

from flask import Flask, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient

# Initialize Flask
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app)

# Configure MongoDB connection via environment variables.
# Prefer MONGODB_URI (sometimes used by hosting providers) and fall back to MONGO_URI.
MONGO_URI = os.environ.get('MONGODB_URI') or os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME', 'notetaker_db')


def init_mongo_client(uri, attempts=3, server_selection_timeout_ms=5000, connect_timeout_ms=10000):
    """Initialize a MongoClient with retries and tuned timeouts.

    - server_selection_timeout_ms controls how long PyMongo will wait for server selection.
    - connect_timeout_ms controls the underlying socket connect timeout.
    The function will try up to `attempts` times (exponential backoff) and will
    exit the process with non-zero code if unable to connect. This avoids long
    import-time blocking and provides clearer diagnostic messages.
    """
    if not uri:
        print('MONGO_URI not set, using default mongodb://localhost:27017')
        uri = 'mongodb://localhost:27017'

    for i in range(attempts):
        try:
            print(f'Attempting MongoDB connection (attempt {i+1}/{attempts})...')
            client = MongoClient(uri, serverSelectionTimeoutMS=server_selection_timeout_ms, connectTimeoutMS=connect_timeout_ms)
            # Force server selection / quick health check
            client.admin.command('ping')
            print('MongoDB connection established')
            return client
        except Exception as e:
            print(f'MongoDB connection attempt {i+1} failed: {e}')
            if i < attempts - 1:
                backoff = min(5, (2 ** i))
                print(f'Retrying in {backoff}s...')
                time.sleep(backoff)

    print(f'Failed to establish MongoDB connection after {attempts} attempts. Exiting.')
    sys.exit(1)


# Initialize the client with short server selection timeout and a few retries
client = init_mongo_client(MONGO_URI, attempts=int(os.environ.get('MONGO_CONNECT_ATTEMPTS', '3')))
db = client[MONGO_DB_NAME]

# Make the db available to routes via app.config
app.config['MONGO_DB'] = db

# register blueprints (import after db is configured to avoid circular imports)
from src.routes.user import user_bp
from src.routes.note import note_bp

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(note_bp, url_prefix='/api')


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
