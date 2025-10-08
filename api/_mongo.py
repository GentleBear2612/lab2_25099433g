import os
import sys
import traceback
import certifi
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from threading import Lock

# Module-level client to allow reuse across serverless invocations when possible
_client = None


def get_client():
    """
    Get MongoDB client. Returns a real MongoDB client if MONGO_URI is set,
    otherwise returns a lightweight in-memory fallback for testing.
    """
    global _client
    if _client is not None:
        return _client

    uri = os.environ.get('MONGO_URI')
    if not uri:
        # Provide a lightweight in-memory fallback client to avoid 500 errors
        # when running in environments without configured MONGO_URI (useful
        # for quick debugging or front-end testing). This fallback is NOT
        # suitable for production (ephemeral, not persisted across invocations).
        class FakeCollection:
            def __init__(self):
                self._docs = []
                self._lock = Lock()

            def find(self, *args, **kwargs):
                # return a shallow copy to mimic cursor iteration
                with self._lock:
                    return list(self._docs)

            def find_one(self, q):
                with self._lock:
                    if not q:
                        return self._docs[0] if self._docs else None
                    # support lookup by _id
                    if isinstance(q.get('_id'), ObjectId):
                        for d in self._docs:
                            if d.get('_id') == q.get('_id'):
                                return d
                    # simple key equality
                    for d in self._docs:
                        ok = True
                        for k, v in q.items():
                            if d.get(k) != v:
                                ok = False
                                break
                        if ok:
                            return d
                    return None

            def insert_one(self, doc):
                with self._lock:
                    new = dict(doc)
                    new['_id'] = ObjectId()
                    # ensure timestamps
                    if 'created_at' not in new:
                        new['created_at'] = datetime.utcnow()
                    if 'updated_at' not in new:
                        new['updated_at'] = new['created_at']
                    self._docs.append(new)
                    class R: pass
                    r = R()
                    r.inserted_id = new['_id']
                    return r

            def delete_one(self, q):
                with self._lock:
                    target = None
                    if isinstance(q.get('_id'), ObjectId):
                        for d in self._docs:
                            if d.get('_id') == q.get('_id'):
                                target = d
                                break
                    if target:
                        self._docs.remove(target)
                        class Res: pass
                        r = Res(); r.deleted_count = 1
                        return r
                    class Res: pass
                    r = Res(); r.deleted_count = 0
                    return r

            def find_one_and_update(self, q, update, return_document=None):
                with self._lock:
                    doc = self.find_one(q)
                    if not doc:
                        return None
                    # apply $set
                    sets = update.get('$set', {})
                    for k, v in sets.items():
                        # support nested translations.* keys
                        if '.' in k:
                            parts = k.split('.')
                            cur = doc
                            for p in parts[:-1]:
                                if p not in cur or not isinstance(cur[p], dict):
                                    cur[p] = {}
                                cur = cur[p]
                            cur[parts[-1]] = v
                        else:
                            doc[k] = v
                    return doc

        class FakeDB:
            def __init__(self):
                self.notes = FakeCollection()
                self.users = FakeCollection()

        class FakeClient:
            def __init__(self):
                self._db = FakeDB()

            def __getitem__(self, name):
                return self._db

            def get_database(self, name):
                return self._db

            def admin(self):
                class A: pass
                return A()

        # warn in logs but allow fallback
        print('WARNING: MONGO_URI not set — using in-memory fallback (ephemeral).', file=sys.stderr)
        _client = FakeClient()
        return _client

    try:
        # Use certifi bundle to improve TLS CA trust consistency across platforms
        _client = MongoClient(uri, serverSelectionTimeoutMS=5000, tlsCAFile=certifi.where())
        # Attempt a quick ping to ensure connectivity
        _client.admin.command('ping')
        return _client
    except Exception as e:
        # Print full traceback to stderr so Vercel captures it in function logs
        traceback.print_exc(file=sys.stderr)
        # raise a clearer runtime error for the caller
        raise RuntimeError(f'Unable to connect to MongoDB: {e}') from e

