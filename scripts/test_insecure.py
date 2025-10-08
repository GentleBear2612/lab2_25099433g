import os, traceback
from pymongo import MongoClient

uri = os.environ.get('MONGO_URI')
if not uri:
    print('MONGO_URI not set')
    raise SystemExit(1)

try:
    client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True, serverSelectionTimeoutMS=5000)
    print('Attempting ping (tlsAllowInvalidCertificates=True) ...')
    print(client.admin.command('ping'))
except Exception:
    print('Exception during insecure ping:')
    traceback.print_exc()
