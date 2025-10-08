import json
from bson import ObjectId
from api._mongo import get_client
import os
from datetime import datetime


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
    try:
        client = get_client()
        db_name = os.environ.get('MONGO_DB_NAME', 'notetaker_db')
        db = client[db_name]
        coll = db.get_collection('notes')

        method = getattr(request, 'method', 'GET').upper()
        idv = _get_id(request)
        if not idv:
            return {'statusCode': 400, 'body': json.dumps({'error': 'id query parameter required'})}

        try:
            oid = ObjectId(idv)
        except Exception:
            return {'statusCode': 400, 'body': json.dumps({'error': 'invalid id'})}

        if method == 'GET':
            doc = coll.find_one({'_id': oid})
            if not doc:
                return {'statusCode': 404, 'body': json.dumps({'error': 'not found'})}
            return {'statusCode': 200, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps(_serialize_doc(doc))}

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
                return {'statusCode': 400, 'body': json.dumps({'error': 'no updatable fields provided'})}
            update['updated_at'] = datetime.utcnow()
            res = coll.find_one_and_update({'_id': oid}, {'$set': update}, return_document=True)
            if not res:
                return {'statusCode': 404, 'body': json.dumps({'error': 'not found'})}
            return {'statusCode': 200, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps(_serialize_doc(res))}

        if method == 'DELETE':
            res = coll.delete_one({'_id': oid})
            if res.deleted_count == 0:
                return {'statusCode': 404, 'body': json.dumps({'error': 'not found'})}
            return {'statusCode': 204, 'body': ''}

        return {'statusCode': 405, 'body': ''}
    except Exception as e:
        import sys, traceback
        traceback.print_exc(file=sys.stderr)
        msg = str(e) or ''
        if isinstance(e, RuntimeError) and 'MONGO_URI' in msg:
            return {'statusCode': 503, 'body': json.dumps({'error': 'Service unavailable', 'detail': 'MONGO_URI environment variable not configured'})}
        return {'statusCode': 500, 'body': json.dumps({'error': msg})}
