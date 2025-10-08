import os
from pymongo import MongoClient
from urllib.parse import urlparse

uri = os.environ.get('MONGO_URI')
print('MONGO_URI environment variable is set:' , bool(uri))
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
    print('MONGO_URI (masked):', masked)
    print('MONGO host extracted from URI:', host)
else:
    print('MONGO_URI not set; defaulting to mongodb://localhost:27017')
    uri = 'mongodb://localhost:27017'

print('Attempting to connect and discover hosts...')
client = MongoClient(uri, serverSelectionTimeoutMS=5000)
try:
    # force server selection
    client.admin.command('ping')
    # PyMongo exposes cluster nodes via client.nodes (set of (host,port)) for standard connections
    nodes = getattr(client, 'nodes', None)
    print('Discovered nodes:', nodes)
    # For SRV, client.address may be None; try client._topology_settings if available
    try:
        ts = client._Toplogy__settings
    except Exception:
        try:
            ts = client._topology_settings
        except Exception:
            ts = None
    print('Topology settings:', ts)
except Exception as e:
    print('Connection failed or timed out:', e)
finally:
    client.close()
