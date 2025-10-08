from pymongo import MongoClient
import os
from bson import ObjectId

MONGO_URI = os.environ.get('MONGODB_URI') or os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
MONGO_DB = os.environ.get('MONGO_DB_NAME', 'notetaker_db')
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

note_id = '68e64bbbb22e9a1b1803a624'
doc = db.notes.find_one({'_id': ObjectId(note_id)})
print('raw document:')
print(doc)
print('\ntranslations field present?', 'translations' in (doc or {}))
