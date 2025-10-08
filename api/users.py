import json
from api._mongo import get_client
import os
from datetime import datetime


def handler(request):
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
            return {'statusCode': 200, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps(result)}

        if method == 'POST':
            try:
                body = request.get_json(silent=True) or {}
            except Exception:
                body = {}
            if not body or 'username' not in body or 'email' not in body:
                return {'statusCode': 400, 'body': json.dumps({'error': 'username and email required'})}
            doc = {'username': body['username'], 'email': body['email'], 'created_at': datetime.utcnow()}
            res = coll.insert_one(doc)
            doc['_id'] = str(res.inserted_id)
            return {'statusCode': 201, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps(doc)}

        return {'statusCode': 405, 'body': ''}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}
