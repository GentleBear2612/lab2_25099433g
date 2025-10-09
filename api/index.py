"""
Vercel serverless function entry point for Flask application.
This file is the entry point for Vercel's Python runtime.
"""
import os
import sys

# Add the parent directory to the path so we can import from src
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

print(f"[Vercel] Python: {sys.version}")
print(f"[Vercel] Current dir: {current_dir}")
print(f"[Vercel] Parent dir: {parent_dir}")
print(f"[Vercel] sys.path[0]: {sys.path[0]}")

# Import Flask app
print("[Vercel] Importing Flask app...")
try:
    from src.main import app
    print("[Vercel] ✓ App imported successfully")
except Exception as e:
    print(f"[Vercel] ✗ Import failed: {e}")
    import traceback
    traceback.print_exc()
    raise

# Export for Vercel
app = app
print("[Vercel] ✓ Ready to serve requests")
