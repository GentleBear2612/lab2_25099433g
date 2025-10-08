#!/usr/bin/env python3
"""Inspect the local SQLite database `database/app.db`: list tables and row counts"""
import os
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / 'database' / 'app.db'

print(f"Checking SQLite DB at: {DB_PATH}")
if not DB_PATH.exists():
    print("DB file does not exist.")
    raise SystemExit(2)

print(f"File size: {DB_PATH.stat().st_size} bytes")

conn = sqlite3.connect(str(DB_PATH))
cur = conn.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
rows = cur.fetchall()
if not rows:
    print("No tables found in the SQLite database.")
    conn.close()
    raise SystemExit(0)

tables = [r[0] for r in rows]
print(f"Found tables: {tables}")

for t in tables:
    try:
        cur.execute(f'SELECT COUNT(*) FROM "{t}"')
        cnt = cur.fetchone()[0]
    except Exception as e:
        cnt = f"error: {e}"
    print(f"  - {t}: {cnt} rows")

conn.close()
