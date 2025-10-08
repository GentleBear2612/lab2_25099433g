from api._mongo import get_client
from datetime import datetime

def main():
    c = get_client()
    db = c['notetaker_db']
    notes = db.get_collection('notes')
    now = datetime.utcnow()
    res = notes.insert_one({'title':'test from smoke','content':'hello sqlite','created_at':now,'updated_at':now,'translations':{}})
    print('inserted id:', res.inserted_id)
    rows = list(notes.find().limit(10))
    print('found rows count:', len(rows))
    for r in rows:
        print('row type:', type(r))
        print('row keys:', list(r.keys()))
        print('created_at type:', type(r.get('created_at')) , 'value:', r.get('created_at'))

if __name__ == '__main__':
    main()
