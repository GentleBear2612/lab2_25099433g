import os
import sys
import traceback
import certifi
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from threading import Lock
import sqlite3
import json
import uuid
from pathlib import Path

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
        # Use SQLite fallback (persistent) when MONGO_URI is not configured.
        # This implements a very small subset of the MongoDB collection API
        # expected by the rest of the code (find, find_one, insert_one,
        # delete_one, find_one_and_update) so the rest of the app doesn't
        # need to change.

        DB_PATH = Path(__file__).resolve().parents[0].parent / 'database' / 'app.db'
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)

        class SQLiteCollection:
            def __init__(self, conn, table):
                self.conn = conn
                self.table = table
                self.lock = Lock()

            def _row_to_doc(self, row):
                if not row:
                    return None
                d = dict(row)
                # unify id field name to _id for compatibility
                if 'id' in d:
                    d['_id'] = d.pop('id')
                # parse json fields
                if 'translations' in d and d['translations']:
                    try:
                        d['translations'] = json.loads(d['translations'])
                    except Exception:
                        d['translations'] = {}
                # parse ISO timestamp strings into datetime objects for compatibility
                for tkey in ('created_at', 'updated_at'):
                    val = d.get(tkey)
                    if isinstance(val, str) and val:
                        try:
                            d[tkey] = datetime.fromisoformat(val)
                        except Exception:
                            # leave as string if parsing fails
                            pass
                return d

            def find(self, *args, **kwargs):
                # return a cursor-like object to support sort().limit()
                cur = self.conn.cursor()
                with self.lock:
                    cur.execute(f"SELECT * FROM {self.table}")
                    rows = [dict(r) for r in cur.fetchall()]
                return SQLCursor(rows)

            def find_one(self, q=None):
                with self.lock:
                    cur = self.conn.cursor()
                    if not q:
                        cur.execute(f"SELECT * FROM {self.table} LIMIT 1")
                        row = cur.fetchone()
                        return self._row_to_doc(row)
                    _id = q.get('_id')
                    if _id is not None:
                        cur.execute(f"SELECT * FROM {self.table} WHERE id = ?", (str(_id),))
                        return self._row_to_doc(cur.fetchone())
                    # fallback simple equality match for single key
                    for k, v in q.items():
                        cur.execute(f"SELECT * FROM {self.table} WHERE {k} = ? LIMIT 1", (v,))
                        row = cur.fetchone()
                        if row:
                            return self._row_to_doc(row)
                    return None

            def insert_one(self, doc):
                with self.lock:
                    _id = str(uuid.uuid4())
                    now = datetime.utcnow().isoformat()
                    title = doc.get('title')
                    content = doc.get('content')
                    created_at = doc.get('created_at')
                    updated_at = doc.get('updated_at')
                    # accept datetime objects
                    if created_at and hasattr(created_at, 'isoformat'):
                        created_at = created_at.isoformat()
                    if updated_at and hasattr(updated_at, 'isoformat'):
                        updated_at = updated_at.isoformat()
                    created_at = created_at or now
                    updated_at = updated_at or created_at
                    translations = doc.get('translations') or {}
                    translations_json = json.dumps(translations)
                    cur = self.conn.cursor()
                    cur.execute(f"INSERT INTO {self.table} (id, title, content, created_at, updated_at, translations) VALUES (?,?,?,?,?,?)",
                                (_id, title, content, created_at, updated_at, translations_json))
                    self.conn.commit()
                    class R: pass
                    r = R(); r.inserted_id = _id
                    return r

            def delete_one(self, q):
                with self.lock:
                    _id = q.get('_id')
                    cur = self.conn.cursor()
                    if _id is None:
                        return type('Res', (), {'deleted_count': 0})()
                    cur.execute(f"DELETE FROM {self.table} WHERE id = ?", (str(_id),))
                    self.conn.commit()
                    return type('Res', (), {'deleted_count': cur.rowcount})()

            def find_one_and_update(self, q, update, return_document=None):
                with self.lock:
                    doc = self.find_one(q)
                    if not doc:
                        return None
                    sets = update.get('$set', {})
                    # apply nested keys like translations.en
                    for k, v in sets.items():
                        if '.' in k:
                            parts = k.split('.')
                            curd = doc
                            for p in parts[:-1]:
                                if p not in curd or not isinstance(curd[p], dict):
                                    curd[p] = {}
                                curd = curd[p]
                            curd[parts[-1]] = v
                        else:
                            doc[k] = v
                    # persist back to db
                    translations = json.dumps(doc.get('translations', {}))
                    # ensure updated_at is an ISO string when saving
                    updated_at_val = doc.get('updated_at')
                    if hasattr(updated_at_val, 'isoformat'):
                        updated_at_val = updated_at_val.isoformat()
                    cur = self.conn.cursor()
                    cur.execute(f"UPDATE {self.table} SET title = ?, content = ?, updated_at = ?, translations = ? WHERE id = ?",
                                (doc.get('title'), doc.get('content'), updated_at_val, translations, str(doc.get('_id'))))
                    self.conn.commit()
                    return doc

        class SQLCursor:
            def __init__(self, rows):
                # rows are plain dicts from sqlite
                self._rows = rows
                self._limit = None

            def sort(self, key, direction=None):
                reverse = True if direction and int(direction) < 0 else False
                # support nested keys but keep simple
                self._rows.sort(key=lambda r: r.get(key) or '', reverse=reverse)
                return self

            def limit(self, n):
                try:
                    self._limit = int(n)
                except Exception:
                    self._limit = None
                return self

            def __iter__(self):
                rows = self._rows
                if self._limit is not None:
                    rows = rows[:self._limit]
                for r in rows:
                    # convert sqlite row dict to expected doc shape
                    d = dict(r)
                    if 'id' in d:
                        d['_id'] = d.pop('id')
                    if 'translations' in d and d['translations']:
                        try:
                            d['translations'] = json.loads(d['translations'])
                        except Exception:
                            d['translations'] = {}
                    # convert ISO timestamps into datetime objects where possible
                    for tkey in ('created_at', 'updated_at'):
                        val = d.get(tkey)
                        if isinstance(val, str) and val:
                            try:
                                d[tkey] = datetime.fromisoformat(val)
                            except Exception:
                                pass
                    yield d

        class SQLiteDB:
            def __init__(self, conn):
                self._conn = conn

            def get_collection(self, name):
                return SQLiteCollection(self._conn, name)

        class SQLiteClient:
            def __init__(self, path):
                # allow access from multiple threads
                self.conn = sqlite3.connect(str(path), check_same_thread=False)
                self.conn.row_factory = sqlite3.Row
                self._ensure_tables()

            def _ensure_tables(self):
                cur = self.conn.cursor()
                cur.execute('''CREATE TABLE IF NOT EXISTS notes (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    content TEXT,
                    created_at TEXT,
                    updated_at TEXT,
                    translations TEXT
                )''')
                cur.execute('''CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    username TEXT,
                    email TEXT,
                    created_at TEXT
                )''')
                self.conn.commit()

            def __getitem__(self, name):
                return SQLiteDB(self.conn)

            def get_database(self, name):
                return SQLiteDB(self.conn)

            def admin(self):
                class A: pass
                return A()

        print('INFO: MONGO_URI not set — using SQLite fallback at %s' % DB_PATH, file=sys.stderr)
        _client = SQLiteClient(DB_PATH)
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

