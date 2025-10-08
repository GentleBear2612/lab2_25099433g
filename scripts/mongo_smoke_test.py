import os
from pymongo import MongoClient
from bson.objectid import ObjectId

MONGO_URI = os.environ.get('MONGO_URI')
MONGO_DB = os.environ.get('MONGO_DB_NAME', 'notetaker_db')

if not MONGO_URI:
    print('MONGO_URI not set')
    raise SystemExit(1)

print('Connecting to MongoDB...')
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
print('Using database:', MONGO_DB)

coll = db.get_collection('notes')

# Insert a temporary document
res = coll.insert_one({'title': 'smoke-test', 'content': 'This is a smoke test', 'created_at': __import__('datetime').datetime.utcnow(), 'updated_at': __import__('datetime').datetime.utcnow()})
print('Inserted id:', str(res.inserted_id))

# Read it back
doc = coll.find_one({'_id': res.inserted_id})
print('Found document title:', doc.get('title'))

# Clean up
coll.delete_one({'_id': res.inserted_id})
print('Deleted test document')
