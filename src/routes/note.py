from flask import Blueprint, jsonify, request, current_app
from src.models.note import doc_to_dict, make_note_doc
from bson import ObjectId
from pymongo import ReturnDocument
from src.llm import translate, generate_note
from datetime import datetime

note_bp = Blueprint('note', __name__)


def notes_collection():
    """Get notes collection with error handling"""
    db = current_app.config.get('MONGO_DB')
    if db is None:
        raise RuntimeError("Database not connected. Please check MONGODB_URI environment variable.")
    return db.notes


@note_bp.route('/notes', methods=['GET'])
def get_notes():
    """Get all notes, ordered by most recently updated"""
    try:
        coll = notes_collection()
        docs = coll.find().sort('updated_at', -1)
        return jsonify([doc_to_dict(d) for d in docs])
    except RuntimeError as e:
        return jsonify({'error': str(e), 'type': 'configuration_error'}), 503
    except Exception as e:
        return jsonify({'error': str(e), 'type': 'server_error'}), 500


@note_bp.route('/notes', methods=['POST'])
def create_note():
    """Create a new note"""
    try:
        data = request.json
        if not data or 'title' not in data or 'content' not in data:
            return jsonify({'error': 'Title and content are required'}), 400

        coll = notes_collection()
        doc = make_note_doc(data['title'], data['content'])
        result = coll.insert_one(doc)
        doc['_id'] = result.inserted_id
        return jsonify(doc_to_dict(doc)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@note_bp.route('/notes/generate', methods=['POST'])
def generate_note_endpoint():
    """Generate a note using the LLM and persist it.

    Request JSON: { "prompt": "..." }
    Response: 201 with created note JSON on success.
    """
    data = request.get_json(silent=True) or {}
    prompt = data.get('prompt')
    if not prompt or not isinstance(prompt, str):
        return jsonify({'error': 'prompt must be a non-empty string'}), 400

    model_name = data.get('model')
    api_token = data.get('token') or data.get('api_token')

    try:
        generated = generate_note(prompt, model_name=model_name, api_token=api_token)
    except Exception as e:
        current_app.logger.exception('LLM generate failed')
        return jsonify({'error': 'LLM generation failed', 'detail': str(e)}), 502

    title = generated.get('title') or ''
    content = generated.get('content') or ''

    doc = make_note_doc(title, content)
    try:
        coll = notes_collection()
        res = coll.insert_one(doc)
        doc['_id'] = res.inserted_id
        return jsonify(doc_to_dict(doc)), 201
    except RuntimeError as re:
        return jsonify({'error': str(re)}), 503
    except Exception as e:
        current_app.logger.exception('Failed to save generated note')
        return jsonify({'error': 'Failed to save generated note', 'detail': str(e)}), 500


@note_bp.route('/notes/<note_id>', methods=['GET'])
def get_note(note_id):
    """Get a specific note by ID"""
    coll = notes_collection()
    try:
        doc = coll.find_one({'_id': ObjectId(note_id)})
    except Exception:
        return jsonify({'error': 'Invalid note id'}), 400
    if not doc:
        return jsonify({'error': 'Note not found'}), 404
    return jsonify(doc_to_dict(doc))


@note_bp.route('/notes/<note_id>', methods=['PUT'])
def update_note(note_id):
    """Update a specific note"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        coll = notes_collection()
        try:
            oid = ObjectId(note_id)
        except Exception:
            return jsonify({'error': 'Invalid note id'}), 400

        update = {}
        if 'title' in data:
            update['title'] = data['title']
        if 'content' in data:
            update['content'] = data['content']
        if 'translations' in data and isinstance(data['translations'], dict):
            # set individual translation keys under translations map
            for k, v in data['translations'].items():
                update[f'translations.{k}'] = v
        if not update:
            return jsonify({'error': 'No updatable fields provided'}), 400

        update['updated_at'] = __import__('datetime').datetime.utcnow()
        result = coll.find_one_and_update({'_id': oid}, {'$set': update}, return_document=ReturnDocument.AFTER)
        if not result:
            return jsonify({'error': 'Note not found'}), 404
        return jsonify(doc_to_dict(result))
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@note_bp.route('/notes/<note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Delete a specific note"""
    coll = notes_collection()
    try:
        oid = ObjectId(note_id)
    except Exception:
        return jsonify({'error': 'Invalid note id'}), 400
    result = coll.delete_one({'_id': oid})
    if result.deleted_count == 0:
        return jsonify({'error': 'Note not found'}), 404
    return '', 204


@note_bp.route('/notes/search', methods=['GET'])
def search_notes():
    """Search notes by title or content"""
    q = request.args.get('q', '')
    if not q:
        return jsonify([])
    coll = notes_collection()
    docs = coll.find({'$or': [{'title': {'$regex': q, '$options': 'i'}}, {'content': {'$regex': q, '$options': 'i'}}]}).sort('updated_at', -1)
    return jsonify([doc_to_dict(d) for d in docs])


@note_bp.route('/notes/<note_id>/translate', methods=['POST'])
def translate_note(note_id):
    """Translate a note's content using the configured LLM.

    Request JSON (optional fields):
    - to: target language (default: English)
    - model: model name to use (optional)
    - token: API token to override environment (optional)

    Response: { id, translated_content }
    """
    coll = notes_collection()
    try:
        doc = coll.find_one({'_id': ObjectId(note_id)})
    except Exception:
        return jsonify({'error': 'Invalid note id'}), 400
    if not doc:
        return jsonify({'error': 'Note not found'}), 404

    data = request.json or {}
    target = data.get('to', 'English')
    model_name = data.get('model')
    token = data.get('token')

    try:
        translated = translate(doc.get('content', ''), target_language=target, model_name=model_name, api_token=token)

        # persist the translation into the note document under a `translations` map
        update_doc = {
            f'translations.{target}': translated,
            'updated_at': datetime.utcnow()
        }
        coll.find_one_and_update({'_id': doc.get('_id')}, {'$set': update_doc}, return_document=ReturnDocument.AFTER)

        return jsonify({'id': str(doc.get('_id')), 'translated_content': translated})
    except RuntimeError as e:
        # Likely API/token errors
        return jsonify({'error': str(e)}), 502
    except Exception as e:
        return jsonify({'error': str(e)}), 500

