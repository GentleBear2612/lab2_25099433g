import os, traceback
import certifi
from pymongo import MongoClient

uri = os.environ.get('MONGO_URI')
if not uri:
    print('MONGO_URI not set')
    raise SystemExit(1)

try:
    client = MongoClient(uri, tls=True, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=5000)
    print('Attempting ping (using certifi CA bundle) ...')
    print(client.admin.command('ping'))
except Exception:
    print('Exception during certifi ping:')
    traceback.print_exc()
