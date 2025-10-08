from datetime import datetime


def user_doc_to_dict(doc):
    if not doc:
        return None
    return {
        'id': str(doc.get('_id')),
        'username': doc.get('username'),
        'email': doc.get('email')
    }


def make_user_doc(username, email):
    return {
        'username': username,
        'email': email,
        'created_at': datetime.utcnow()
    }
