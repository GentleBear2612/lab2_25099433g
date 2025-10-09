from flask import Blueprint, jsonify, request, current_app
from src.models.user import user_doc_to_dict, make_user_doc
from bson import ObjectId

user_bp = Blueprint('user', __name__)


def users_collection():
    """Get users collection with error handling"""
    db = current_app.config.get('MONGO_DB')
    if db is None:
        raise RuntimeError("Database not connected. Please check MONGODB_URI environment variable.")
    return db.users


@user_bp.route('/users', methods=['GET'])
def get_users():
    try:
        coll = users_collection()
        docs = coll.find()
        return jsonify([user_doc_to_dict(d) for d in docs])
    except RuntimeError as e:
        return jsonify({'error': str(e), 'type': 'configuration_error'}), 503
    except Exception as e:
        return jsonify({'error': str(e), 'type': 'server_error'}), 500


@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if not data or 'username' not in data or 'email' not in data:
        return jsonify({'error': 'username and email required'}), 400
    coll = users_collection()
    doc = make_user_doc(data['username'], data['email'])
    result = coll.insert_one(doc)
    doc['_id'] = result.inserted_id
    return jsonify(user_doc_to_dict(doc)), 201


@user_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    coll = users_collection()
    try:
        doc = coll.find_one({'_id': ObjectId(user_id)})
    except Exception:
        return jsonify({'error': 'Invalid user id'}), 400
    if not doc:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user_doc_to_dict(doc))


@user_bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    coll = users_collection()
    data = request.json or {}
    try:
        oid = ObjectId(user_id)
    except Exception:
        return jsonify({'error': 'Invalid user id'}), 400
    update = {}
    if 'username' in data:
        update['username'] = data['username']
    if 'email' in data:
        update['email'] = data['email']
    if not update:
        return jsonify({'error': 'No updatable fields provided'}), 400
    result = coll.find_one_and_update({'_id': oid}, {'$set': update}, return_document=True)
    if not result:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user_doc_to_dict(result))


@user_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    coll = users_collection()
    try:
        oid = ObjectId(user_id)
    except Exception:
        return jsonify({'error': 'Invalid user id'}), 400
    result = coll.delete_one({'_id': oid})
    if result.deleted_count == 0:
        return jsonify({'error': 'User not found'}), 404
    return '', 204
