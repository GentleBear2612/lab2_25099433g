import json
import os
import sys
from datetime import datetime

# Import from same directory (relative import for Vercel compatibility)
try:
    from ._mongo import get_client
except ImportError:
    from _mongo import get_client


def handler(request):
    """Handles GET (list) and POST (create) for /api/users"""
    from flask import Response
    
    try:
        client = get_client()
        db_name = os.environ.get('MONGO_DB_NAME', 'notetaker_db')
        db = client[db_name]
        coll = db.get_collection('users')
        method = getattr(request, 'method', 'GET').upper()

        if method == 'GET':
            docs = list(coll.find().limit(50))
            # simple serialization
            result = []
            for d in docs:
                d['_id'] = str(d.get('_id'))
                result.append(d)
            return Response(
                json.dumps(result),
                status=200,
                mimetype='application/json',
                headers={'Access-Control-Allow-Origin': '*'}
            )

        if method == 'POST':
            try:
                body = request.get_json(silent=True) or {}
            except Exception:
                body = {}
            if not body or 'username' not in body or 'email' not in body:
                return Response(
                    json.dumps({'error': 'username and email required'}),
                    status=400,
                    mimetype='application/json',
                    headers={'Access-Control-Allow-Origin': '*'}
                )
            doc = {'username': body['username'], 'email': body['email'], 'created_at': datetime.utcnow()}
            res = coll.insert_one(doc)
            doc['_id'] = str(res.inserted_id)
            return Response(
                json.dumps(doc),
                status=201,
                mimetype='application/json',
                headers={'Access-Control-Allow-Origin': '*'}
            )

        return Response('', status=405, headers={'Access-Control-Allow-Origin': '*'})
        
    except Exception as e:
        import sys, traceback
        traceback.print_exc(file=sys.stderr)
        msg = str(e) or ''
        if isinstance(e, RuntimeError) and 'MONGO_URI' in msg:
            return Response(
                json.dumps({'error': 'Service unavailable', 'detail': 'MONGO_URI environment variable not configured'}),
                status=503,
                mimetype='application/json',
                headers={'Access-Control-Allow-Origin': '*'}
            )
        return Response(
            json.dumps({'error': str(e)}),
            status=500,
            mimetype='application/json',
            headers={'Access-Control-Allow-Origin': '*'}
        )

# Vercel entry point
def main(request):
    """Vercel serverless function entry point"""
    return handler(request)
