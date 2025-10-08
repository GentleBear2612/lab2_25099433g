import os
import certifi
from pymongo import MongoClient

# Module-level client to allow reuse across serverless invocations when possible
_client = None

def get_client():
    global _client
    if _client is not None:
        return _client

    uri = os.environ.get('MONGO_URI')
    if not uri:
        raise RuntimeError('MONGO_URI environment variable is not set')

    # Use certifi bundle to improve TLS CA trust consistency across platforms
    _client = MongoClient(uri, serverSelectionTimeoutMS=5000, tlsCAFile=certifi.where())
    # Attempt a quick ping to ensure connectivity
    _client.admin.command('ping')
    return _client

