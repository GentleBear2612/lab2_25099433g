import json
from bson import ObjectId
from api._mongo import get_client
import os
from datetime import datetime


def handler(request):
    """Handles single user operations: GET, PUT, DELETE"""
    from flask import Response
    
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
            return Response(
                json.dumps({'error': 'id required'}),
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

        method = getattr(request, 'method', 'GET').upper()
        if method == 'GET':
            doc = coll.find_one({'_id': oid})
            if not doc:
                return Response(
                    json.dumps({'error': 'not found'}),
                    status=404,
                    mimetype='application/json',
                    headers={'Access-Control-Allow-Origin': '*'}
                )
            doc['_id'] = str(doc['_id'])
            return Response(
                json.dumps(doc),
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
            if 'username' in body:
                update['username'] = body['username']
            if 'email' in body:
                update['email'] = body['email']
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
            res['_id'] = str(res['_id'])
            return Response(
                json.dumps(res),
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
            json.dumps({'error': str(e)}),
            status=500,
            mimetype='application/json',
            headers={'Access-Control-Allow-Origin': '*'}
        )
