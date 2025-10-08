import json
from bson import ObjectId
from api._mongo import get_client
import os
from datetime import datetime


def handler(request):
    try:
        client = get_client()
        db_name = os.environ.get('MONGO_DB_NAME', 'notetaker_db')
        db = client[db_name]
        coll = db.get_collection('users')

        # id via ?id=<id>
        idv = None
        try:
            if hasattr(request, 'args'):
                idv = request.args.get('id')
        except Exception:
            pass
        if not idv:
            return {'statusCode': 400, 'body': json.dumps({'error': 'id required'})}

        try:
            oid = ObjectId(idv)
        except Exception:
            return {'statusCode': 400, 'body': json.dumps({'error': 'invalid id'})}

        method = getattr(request, 'method', 'GET').upper()
        if method == 'GET':
            doc = coll.find_one({'_id': oid})
            if not doc:
                return {'statusCode': 404, 'body': json.dumps({'error': 'not found'})}
            doc['_id'] = str(doc['_id'])
            return {'statusCode': 200, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps(doc)}

        if method == 'PUT':
            try:
                body = request.get_json(silent=True) or {}
            except Exception:
                body = {}
            update = {}
            if 'username' in body:
                update['username'] = body['username']
            if 'email' in body:
                update['email'] = body['email']
            if not update:
                return {'statusCode': 400, 'body': json.dumps({'error': 'no updatable fields provided'})}
            update['updated_at'] = datetime.utcnow()
            res = coll.find_one_and_update({'_id': oid}, {'$set': update}, return_document=True)
            if not res:
                return {'statusCode': 404, 'body': json.dumps({'error': 'not found'})}
            res['_id'] = str(res['_id'])
            return {'statusCode': 200, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps(res)}

        if method == 'DELETE':
            res = coll.delete_one({'_id': oid})
            if res.deleted_count == 0:
                return {'statusCode': 404, 'body': json.dumps({'error': 'not found'})}
            return {'statusCode': 204, 'body': ''}

        return {'statusCode': 405, 'body': ''}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}
