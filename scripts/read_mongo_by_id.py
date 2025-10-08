import sys
from pymongo import MongoClient
from bson import ObjectId
import os

if len(sys.argv) < 2:
    print('Usage: python read_mongo_by_id.py <objectid>')
    sys.exit(2)

note_id = sys.argv[1]
# Prefer MONGODB_URI, fall back to MONGO_URI, then to localhost
MONGO_URI = os.environ.get('MONGODB_URI') or os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
MONGO_DB = os.environ.get('MONGO_DB_NAME', 'notetaker_db')
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
try:
    doc = db.notes.find_one({'_id': ObjectId(note_id)})
    print('raw document from mongo:')
    print(doc)
except Exception as e:
    print('error reading mongo:', e)
