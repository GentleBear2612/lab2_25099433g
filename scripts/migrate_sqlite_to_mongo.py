"""Migrate notes and users from local SQLite (database/app.db) to MongoDB.

Usage:
    python migrate_sqlite_to_mongo.py --dry-run
    python migrate_sqlite_to_mongo.py --commit

Environment variables:
    MONGO_URI (required)
    MONGO_DB_NAME (optional, default: notetaker_db)

The script will not delete existing MongoDB data. When --commit is used, it will insert documents
and set a field `sqlite_id` on migrated documents to track original IDs.
"""
import os
import sqlite3
import argparse
from datetime import datetime

from pymongo import MongoClient
from bson.objectid import ObjectId

ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
SQLITE_PATH = os.path.join(ROOT, 'database', 'app.db')


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--dry-run', action='store_true', help='Show stats and example rows without writing')
    p.add_argument('--commit', action='store_true', help='Perform the migration and write to MongoDB')
    return p.parse_args()


def parse_sqlite_timestamp(val):
    if not val:
        return None
    # Try common formats
    for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(val, fmt)
        except Exception:
            pass
    try:
        return datetime.fromisoformat(val)
    except Exception:
        return None


def load_sqlite_data():
    if not os.path.exists(SQLITE_PATH):
        raise FileNotFoundError(f"SQLite DB not found at {SQLITE_PATH}")
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Fetch notes
    notes = []
    try:
        cur.execute('SELECT id, title, content, created_at, updated_at FROM note')
        notes = [dict(r) for r in cur.fetchall()]
    except sqlite3.OperationalError:
        # table not found -> empty
        notes = []

    # Fetch users
    users = []
    try:
        cur.execute('SELECT id, username, email FROM "user"')
        users = [dict(r) for r in cur.fetchall()]
    except sqlite3.OperationalError:
        users = []

    conn.close()
    return notes, users


def migrate(notes, users, mongo_db, do_commit=False):
    notes_coll = mongo_db.get_collection('notes')
    users_coll = mongo_db.get_collection('users')

    report = {'notes_count': len(notes), 'users_count': len(users), 'notes_inserted': 0, 'users_inserted': 0}

    if not do_commit:
        # show examples
        sample_note = notes[0] if notes else None
        sample_user = users[0] if users else None
        return report, sample_note, sample_user

    # Insert users (skip duplicates by username or email)
    for u in users:
        query = {'$or': [{'username': u.get('username')}, {'email': u.get('email')}]} if (u.get('username') or u.get('email')) else {}
        if query and users_coll.find_one(query):
            continue
        doc = {
            'username': u.get('username'),
            'email': u.get('email'),
            'sqlite_id': u.get('id'),
            'created_at': datetime.utcnow()
        }
        users_coll.insert_one(doc)
        report['users_inserted'] += 1

    # Insert notes
    for n in notes:
        doc = {
            'title': n.get('title') or 'Untitled',
            'content': n.get('content') or '',
            'sqlite_id': n.get('id'),
            'created_at': parse_sqlite_timestamp(n.get('created_at')) or datetime.utcnow(),
            'updated_at': parse_sqlite_timestamp(n.get('updated_at')) or datetime.utcnow()
        }
        notes_coll.insert_one(doc)
        report['notes_inserted'] += 1

    return report, None, None


def main():
    args = parse_args()
    MONGO_URI = os.environ.get('MONGO_URI')
    MONGO_DB = os.environ.get('MONGO_DB_NAME', 'notetaker_db')

    if not MONGO_URI:
        print('MONGO_URI not set. Set environment variable MONGO_URI to your MongoDB connection string and retry.')
        return 2

    notes, users = load_sqlite_data()
    print(f'Found {len(notes)} notes and {len(users)} users in SQLite at {SQLITE_PATH}')

    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]

    report, sample_note, sample_user = migrate(notes, users, db, do_commit=args.commit)

    print('Migration report:')
    print(f"  notes to migrate: {report['notes_count']}")
    print(f"  users to migrate: {report['users_count']}")
    if args.commit:
        print(f"  notes inserted: {report['notes_inserted']}")
        print(f"  users inserted: {report['users_inserted']}")
    else:
        print('Dry run mode - no changes written')
        if sample_note:
            print('Example note:', {k: sample_note.get(k) for k in ('id','title')})
        if sample_user:
            print('Example user:', {k: sample_user.get(k) for k in ('id','username')})

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
