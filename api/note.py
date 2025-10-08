import json
from bson import ObjectId
from api._mongo import get_client
import os
from datetime import datetime
from flask import Flask, Response

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


def _get_id(request):
    # support ?id=<id> or path-like /api/note/<id> via raw url
    idv = None
    try:
        if hasattr(request, 'args'):
            idv = request.args.get('id')
            if idv:
                return idv
    except Exception:
        pass
    try:
        url = getattr(request, 'url', '') or getattr(request, 'raw_url', '')
        if url and '/' in url:
            parts = url.rstrip('/').split('/')
            if parts and parts[-1]:
                return parts[-1]
    except Exception:
        pass
    return None


def handler(request):
    """Handles single note operations: GET, PUT, DELETE"""
    from flask import Response
    
    try:
        client = get_client()
        db_name = os.environ.get('MONGO_DB_NAME', 'notetaker_db')
        db = client[db_name]
        coll = db.get_collection('notes')

        method = getattr(request, 'method', 'GET').upper()
        idv = _get_id(request)
        if not idv:
            return Response(
                json.dumps({'error': 'id query parameter required'}),
                status=400,
                mimetype='application/json',
                headers={'Access-Control-Allow-Origin': '*'}
            )

        try:
            oid = ObjectId(idv)
        except Exception:
            return Response(
                json.dumps({'error': 'invalid id'}),
                status=400,
                mimetype='application/json',
                headers={'Access-Control-Allow-Origin': '*'}
            )

        if method == 'GET':
            doc = coll.find_one({'_id': oid})
            if not doc:
                return Response(
                    json.dumps({'error': 'not found'}),
                    status=404,
                    mimetype='application/json',
                    headers={'Access-Control-Allow-Origin': '*'}
                )
            return Response(
                json.dumps(_serialize_doc(doc)),
                status=200,
                mimetype='application/json',
                headers={'Access-Control-Allow-Origin': '*'}
            )

        if method == 'PUT':
            try:
                body = request.get_json(silent=True) or {}
            except Exception:
                body = {}
            update = {}
            if 'title' in body:
                update['title'] = body['title']
            if 'content' in body:
                update['content'] = body['content']
            if not update:
                return Response(
                    json.dumps({'error': 'no updatable fields provided'}),
                    status=400,
                    mimetype='application/json',
                    headers={'Access-Control-Allow-Origin': '*'}
                )
            update['updated_at'] = datetime.utcnow()
            res = coll.find_one_and_update({'_id': oid}, {'$set': update}, return_document=True)
            if not res:
                return Response(
                    json.dumps({'error': 'not found'}),
                    status=404,
                    mimetype='application/json',
                    headers={'Access-Control-Allow-Origin': '*'}
                )
            return Response(
                json.dumps(_serialize_doc(res)),
                status=200,
                mimetype='application/json',
                headers={'Access-Control-Allow-Origin': '*'}
            )

        if method == 'DELETE':
            res = coll.delete_one({'_id': oid})
            if res.deleted_count == 0:
                return Response(
                    json.dumps({'error': 'not found'}),
                    status=404,
                    mimetype='application/json',
                    headers={'Access-Control-Allow-Origin': '*'}
                )
            return Response('', status=204, headers={'Access-Control-Allow-Origin': '*'})

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
            json.dumps({'error': msg}),
            status=500,
            mimetype='application/json',
            headers={'Access-Control-Allow-Origin': '*'}
        )

# Vercel entry point
def main(request):
    """Vercel serverless function entry point"""
    return handler(request)
