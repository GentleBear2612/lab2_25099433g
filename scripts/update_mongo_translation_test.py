from pymongo import MongoClient
from bson import ObjectId
import os

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
MONGO_DB = os.environ.get('MONGO_DB_NAME', 'notetaker_db')
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

note_id = ObjectId('68e64bbbb22e9a1b1803a624')
res = db.notes.update_one({'_id': note_id}, {'$set': {'translations.TestWrite': '直接写入测试'}})
print('matched:', res.matched_count, 'modified:', res.modified_count)
print('doc now:')
print(db.notes.find_one({'_id': note_id}))
