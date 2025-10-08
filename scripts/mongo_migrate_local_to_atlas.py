"""Migrate data from local MongoDB to Atlas MongoDB.

Usage:
  python mongo_migrate_local_to_atlas.py --dry-run
  python mongo_migrate_local_to_atlas.py --commit

Behavior:
- Connects to local MongoDB at mongodb://localhost:27017 and reads `notetaker_db.notes` and `notetaker_db.users` (if present).
- Connects to target Atlas via MONGO_URI env var (or command-line param) and writes documents into same-named collections.
- Adds metadata fields to migrated documents: `migrated_from: 'local'` and `local_id` (string of original _id).
- Skips documents already migrated (where target has `local_id` equal to original id).
- Default mode is dry-run: shows counts and sample documents without writing.
"""

import argparse
import os
from pymongo import MongoClient
from bson import ObjectId
import json


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--dry-run', action='store_true', help='Show what would be migrated')
    p.add_argument('--commit', action='store_true', help='Perform migration')
    # Prefer MONGODB_URI but fall back to MONGO_URI for compatibility
    p.add_argument('--target-uri', default=(os.environ.get('MONGODB_URI') or os.environ.get('MONGO_URI')), help='Target MongoDB URI (Atlas). Defaults to MONGODB_URI or MONGO_URI env var')
    p.add_argument('--target-db', default=os.environ.get('MONGO_DB_NAME','notetaker_db'))
    p.add_argument('--local-uri', default='mongodb://localhost:27017', help='Local MongoDB URI')
    return p.parse_args()


def sample_docs(docs, n=3):
    res = []
    for i, d in enumerate(docs):
        if i >= n:
            break
        out = {}
        for k, v in d.items():
            if isinstance(v, ObjectId):
                out[k] = str(v)
            else:
                try:
                    out[k] = str(v) if getattr(v, 'isoformat', None) else v
                except Exception:
                    out[k] = str(v)
        res.append(out)
    return res


def main():
    args = parse_args()
    if not args.dry_run and not args.commit:
        print('Specify --dry-run or --commit')
        return
    if not args.target_uri:
        print('Error: target URI not provided. Set MONGODB_URI / MONGO_URI env var or pass --target-uri')
        return

    print('Local URI:', args.local_uri)
    print('Target URI (masked):', mask_uri(args.target_uri))
    print('Target DB:', args.target_db)

    local_client = MongoClient(args.local_uri)
    target_client = MongoClient(args.target_uri)

    local_db = local_client[args.target_db]
    target_db = target_client[args.target_db]

    notes = list(local_db.notes.find())
    users = list(local_db.users.find()) if 'users' in local_db.list_collection_names() else []

    print(f'Found {len(notes)} notes and {len(users)} users in local database')
    print('\nSample notes:')
    print(json.dumps(sample_docs(notes), ensure_ascii=False, indent=2))
    if users:
        print('\nSample users:')
        print(json.dumps(sample_docs(users), ensure_ascii=False, indent=2))

    if args.dry_run:
        print('\nDry-run mode: no changes will be made. To migrate, re-run with --commit')
        return

    # commit mode
    migrated_notes = 0
    migrated_users = 0

    for n in notes:
        local_id = str(n.get('_id'))
        # skip if already migrated
        if target_db.notes.find_one({'local_id': local_id}):
            continue
        doc = n.copy()
        doc['local_id'] = local_id
        doc['migrated_from'] = 'local'
        # remove existing _id so Mongo will assign a new one in target
        if '_id' in doc:
            del doc['_id']
        target_db.notes.insert_one(doc)
        migrated_notes += 1

    for u in users:
        local_id = str(u.get('_id'))
        if target_db.users.find_one({'local_id': local_id}):
            continue
        doc = u.copy()
        doc['local_id'] = local_id
        doc['migrated_from'] = 'local'
        if '_id' in doc:
            del doc['_id']
        target_db.users.insert_one(doc)
        migrated_users += 1

    print(f'Committed migration: inserted {migrated_notes} notes and {migrated_users} users into target DB')


def mask_uri(uri):
    if not uri:
        return ''
    try:
        if '//' in uri and '@' in uri:
            start = uri.find('//')+2
            at = uri.rfind('@')
            credential = uri[start:at]
            if ':' in credential:
                user, pwd = credential.split(':',1)
                return uri.replace(credential, user+':<redacted>')
    except Exception:
        pass
    return uri


if __name__ == '__main__':
    main()
