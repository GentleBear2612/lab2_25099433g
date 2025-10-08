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
    """Handles GET (list) and POST (create) for /api/notes"""
    try:
        client = get_client()
        db_name = os.environ.get('MONGO_DB_NAME', 'notetaker_db')
        db = client[db_name]
        coll = db.get_collection('notes')

        method = getattr(request, 'method', 'GET').upper()
        if method == 'GET':
            docs = list(coll.find().sort('updated_at', -1).limit(50))
            result = [_serialize_doc(d) for d in docs]
            return {'statusCode': 200, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps(result)}

        if method == 'POST':
            data = _parse_json_body(request) or {}
            if not data or 'title' not in data or 'content' not in data:
                return {'statusCode': 400, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps({'error': 'title and content required'})}

            now = datetime.utcnow()
            doc = {'title': data.get('title'), 'content': data.get('content'), 'created_at': now, 'updated_at': now, 'translations': {}}
            res = coll.insert_one(doc)
            doc['_id'] = res.inserted_id
            return {'statusCode': 201, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps(_serialize_doc(doc))}

        return {'statusCode': 405, 'headers': {'Allow': 'GET, POST'}, 'body': ''}
    except Exception as e:
        return {'statusCode': 500, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps({'error': str(e)})}
