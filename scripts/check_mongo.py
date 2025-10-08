import os
from pymongo import MongoClient

MONGO_URI = os.environ.get('MONGO_URI')
MONGO_DB = os.environ.get('MONGO_DB_NAME', 'notetaker_db')

if not MONGO_URI:
    print('MONGO_URI not set')
    raise SystemExit(1)

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

print('Checking database:', MONGO_DB)
colls = db.list_collection_names()
print('Collections:', colls)

for c in ['notes', 'users']:
    if c in colls:
        coll = db.get_collection(c)
        count = coll.count_documents({})
        print(f"{c} count: {count}")
        if count > 0 and c == 'notes':
            doc = coll.find_one({}, projection={'title':1, 'content':1})
            title = doc.get('title') if doc else None
            print(f"Sample note title: {title}")
    else:
        print(f"{c} collection: not found")
