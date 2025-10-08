import json
from bson import ObjectId
from api._mongo import get_client
import os
from datetime import datetime
from flask import Flask, Response, request as flask_request

# Create a minimal Flask app for Vercel
app = Flask(__name__)


def _serialize_doc(d):
    out = {}
    for k, v in d.items():
        if isinstance(v, ObjectId):
            out[k] = str(v)
        else:
            try:
                json.dumps({"v": v})
                out[k] = v
            except Exception:
                out[k] = str(v)
    return out


def _parse_json_body(request):
    # Robust JSON body parsing for different request shapes in serverless envs
    try:
        if hasattr(request, 'json') and request.json is not None:
            return request.json
        if hasattr(request, 'get_json'):
            return request.get_json(silent=True) or {}
        if hasattr(request, 'body'):
            b = request.body
            if isinstance(b, bytes):
                s = b.decode('utf-8')
            else:
                s = str(b)
            return json.loads(s) if s else {}
        if hasattr(request, 'text'):
            s = request.text
            return json.loads(s) if s else {}
    except Exception:
        return {}
    return {}


def _get_query_param(request, name):
    # Try common request attributes to find query params
    for attr in ('args', 'params', 'query'):
        q = getattr(request, attr, None)
        if q:
            try:
                val = q.get(name)
                if val:
                    return val
            except Exception:
                pass
    # Fallback to parsing raw url if present
    try:
        url = getattr(request, 'url', None) or getattr(request, 'raw_url', None)
        if url and ('?' in url):
            from urllib.parse import parse_qs, urlparse
            qs = parse_qs(urlparse(url).query)
            vals = qs.get(name)
            if vals:
                return vals[0]
    except Exception:
        pass
    return None


def handler(request):
    """Handles GET (list) and POST (create) for /api/notes
    This is a Vercel serverless function handler.
    """
    try:
        client = get_client()
        db_name = os.environ.get('MONGO_DB_NAME', 'notetaker_db')
        db = client[db_name]
        coll = db.get_collection('notes')

        method = getattr(request, 'method', 'GET').upper()
        if method == 'GET':
            docs = list(coll.find().sort('updated_at', -1).limit(50))
            result = [_serialize_doc(d) for d in docs]
            return Response(
                json.dumps(result),
                status=200,
                mimetype='application/json',
                headers={'Access-Control-Allow-Origin': '*'}
            )

        if method == 'POST':
            data = _parse_json_body(request) or {}
            if not data or 'title' not in data or 'content' not in data:
                return Response(
                    json.dumps({'error': 'title and content required'}),
                    status=400,
                    mimetype='application/json',
                    headers={'Access-Control-Allow-Origin': '*'}
                )

            now = datetime.utcnow()
            doc = {'title': data.get('title'), 'content': data.get('content'), 'created_at': now, 'updated_at': now, 'translations': {}}
            res = coll.insert_one(doc)
            doc['_id'] = res.inserted_id
            return Response(
                json.dumps(_serialize_doc(doc)),
                status=201,
                mimetype='application/json',
                headers={'Access-Control-Allow-Origin': '*'}
            )

        return Response('', status=405, headers={'Allow': 'GET, POST'})
        
    except Exception as e:
        # Import here to avoid adding logging dependency at module import time
        import sys, traceback
        traceback.print_exc(file=sys.stderr)
        msg = str(e) or ''
        # If missing MONGO_URI, return 503 to indicate service unavailable due to config
        if isinstance(e, RuntimeError) and 'MONGO_URI' in msg:
            return Response(
                json.dumps({'error': 'Service unavailable', 'detail': 'MONGO_URI environment variable not configured'}),
                status=503,
                mimetype='application/json',
                headers={'Access-Control-Allow-Origin': '*'}
            )
        # include short hint in response body to help debugging from client side logs
        return Response(
            json.dumps({'error': 'Internal server error', 'detail': msg}),
            status=500,
            mimetype='application/json',
            headers={'Access-Control-Allow-Origin': '*'}
        )

# Vercel entry point - must be at module level
# This allows Vercel's Python runtime to properly invoke the function
def main(request):
    """Vercel serverless function entry point"""
    return handler(request)
