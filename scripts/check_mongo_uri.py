import os
from pymongo import MongoClient
from urllib.parse import urlparse
import traceback

uri = os.environ.get('MONGODB_URI') or os.environ.get('MONGO_URI')
print('MONGODB_URI / MONGO_URI environment variable is set:' , bool(uri))
if uri:
    # mask credentials when printing
    try:
        parsed = urlparse(uri)
        host = parsed.hostname
    except Exception:
        host = None
    masked = uri
    # mask password if present
    if '//' in uri and '@' in uri:
        start = uri.find('//')+2
        at = uri.rfind('@')
        credential = uri[start:at]
        if ':' in credential:
            user, pwd = credential.split(':',1)
            masked = uri.replace(credential, user+':<redacted>')
    print('MONGODB_URI / MONGO_URI (masked):', masked)
    print('Mongo host extracted from URI:', host)
else:
    print('MONGODB_URI / MONGO_URI not set; defaulting to mongodb://localhost:27017')
    uri = 'mongodb://localhost:27017'

try:
    print('Attempting to connect and discover hosts...')
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    try:
        # force server selection
        client.admin.command('ping')
        nodes = getattr(client, 'nodes', None)
        print('Discovered nodes:', nodes)
        ts = getattr(client, '_topology_settings', None)
        if ts is None:
            ts = getattr(client, '_Topology__settings', None)
        print('Topology settings (internal):', ts)
    except Exception as e:
        print('Connection failed or timed out:', e)
        traceback.print_exc()
    finally:
        client.close()
except Exception as e:
    print('An unexpected error occurred:', e)
    traceback.print_exc()
