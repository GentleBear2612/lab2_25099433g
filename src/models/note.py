from datetime import datetime
from bson import ObjectId


def doc_to_dict(doc):
    if not doc:
        return None
    return {
        'id': str(doc.get('_id')),
        'title': doc.get('title', ''),
        'content': doc.get('content', ''),
        'created_at': doc.get('created_at').isoformat() if doc.get('created_at') else None,
        'updated_at': doc.get('updated_at').isoformat() if doc.get('updated_at') else None,
        'translations': doc.get('translations', {})
    }


def make_note_doc(title, content):
    now = datetime.utcnow()
    return {
        'title': title,
        'content': content,
        'created_at': now,
        'updated_at': now
    }

