"""
Simplified Vercel-compatible handler for /api/notes
This version is specifically optimized for Vercel's Python runtime
"""
import json
import os
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bson import ObjectId
from api._mongo import get_client


def serialize_doc(doc):
    """Convert MongoDB document to JSON-serializable dict"""
    result = {}
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            result[key] = str(value)
        elif isinstance(value, datetime):
            result[key] = value.isoformat()
        else:
            try:
                json.dumps({"test": value})
                result[key] = value
            except (TypeError, ValueError):
                result[key] = str(value)
    return result


def create_response(body, status=200, content_type='application/json'):
    """Create a Vercel-compatible HTTP response"""
    headers = {
        'Content-Type': content_type,
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }
    
    # Return response in the format Vercel expects
    from flask import Response
    return Response(
        response=body if isinstance(body, str) else json.dumps(body),
        status=status,
        headers=headers,
        mimetype=content_type
    )


def get_request_json(request):
    """Safely extract JSON from request"""
    try:
        if hasattr(request, 'get_json'):
            data = request.get_json(silent=True, force=True)
            if data:
                return data
        if hasattr(request, 'json') and request.json:
            return request.json
        if hasattr(request, 'data'):
            data_bytes = request.data
            if data_bytes:
                return json.loads(data_bytes.decode('utf-8'))
        if hasattr(request, 'body'):
            body = request.body
            if isinstance(body, bytes):
                return json.loads(body.decode('utf-8'))
            elif isinstance(body, str):
                return json.loads(body)
    except Exception as e:
        print(f"Error parsing JSON: {e}", file=sys.stderr)
    return {}


def handler(request):
    """Main handler for /api/notes endpoint"""
    try:
        # Get HTTP method
        method = getattr(request, 'method', 'GET').upper()
        
        # Handle OPTIONS for CORS preflight
        if method == 'OPTIONS':
            return create_response('', status=204)
        
        # Get MongoDB client and collection
        client = get_client()
        db_name = os.environ.get('MONGO_DB_NAME', 'notetaker_db')
        db = client[db_name]
        notes_collection = db['notes']
        
        # Handle GET request - list all notes
        if method == 'GET':
            try:
                cursor = notes_collection.find().sort('updated_at', -1).limit(50)
                notes = [serialize_doc(doc) for doc in cursor]
                return create_response(notes, status=200)
            except Exception as e:
                print(f"Error fetching notes: {e}", file=sys.stderr)
                import traceback
                traceback.print_exc(file=sys.stderr)
                return create_response(
                    {'error': 'Failed to fetch notes', 'detail': str(e)},
                    status=500
                )
        
        # Handle POST request - create new note
        elif method == 'POST':
            try:
                data = get_request_json(request)
                
                # Validate required fields
                if not data or 'title' not in data or 'content' not in data:
                    return create_response(
                        {'error': 'Missing required fields: title and content'},
                        status=400
                    )
                
                # Create note document
                now = datetime.utcnow()
                note_doc = {
                    'title': data['title'],
                    'content': data['content'],
                    'created_at': now,
                    'updated_at': now,
                    'translations': {}
                }
                
                # Insert into database
                result = notes_collection.insert_one(note_doc)
                note_doc['_id'] = result.inserted_id
                
                return create_response(serialize_doc(note_doc), status=201)
                
            except Exception as e:
                print(f"Error creating note: {e}", file=sys.stderr)
                import traceback
                traceback.print_exc(file=sys.stderr)
                return create_response(
                    {'error': 'Failed to create note', 'detail': str(e)},
                    status=500
                )
        
        # Method not allowed
        else:
            return create_response(
                {'error': f'Method {method} not allowed'},
                status=405
            )
            
    except Exception as e:
        # Top-level error handler
        print(f"Fatal error in handler: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        
        # Check if it's a MongoDB connection error
        error_msg = str(e)
        if 'MONGO_URI' in error_msg or 'MONGODB_URI' in error_msg or 'Unable to connect' in error_msg:
            return create_response(
                {
                    'error': 'Database connection failed',
                    'detail': 'MONGODB_URI (preferred) or MONGO_URI environment variable may not be configured properly',
                    'hint': 'Check Vercel environment variables and ensure MONGODB_URI is set for production (or MONGO_URI for legacy)'
                },
                status=503
            )
        
        return create_response(
            {'error': 'Internal server error', 'detail': error_msg},
            status=500
        )


# Vercel entry points - try multiple names for compatibility
def main(request):
    """Primary Vercel entry point"""
    return handler(request)

def index(request):
    """Alternative Vercel entry point"""
    return handler(request)

# For local testing
if __name__ == '__main__':
    print("This module is designed to run as a Vercel serverless function")
    print("For local testing, use scripts/test_api_response.py")
