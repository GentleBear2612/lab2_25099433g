from pymongo import MongoClient
import os
from bson import ObjectId
import json

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
MONGO_DB = os.environ.get('MONGO_DB_NAME', 'notetaker_db')
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

notes = list(db.notes.find().sort('updated_at', -1))
print(f"Found {len(notes)} notes in database '{MONGO_DB}'")
for n in notes:
    out = {
        '_id': str(n.get('_id')),
        'title': n.get('title'),
        'content': n.get('content'),
        'translations': n.get('translations', {}),
        'created_at': n.get('created_at'),
        'updated_at': n.get('updated_at')
    }
    print(json.dumps(out, default=str, ensure_ascii=False))
