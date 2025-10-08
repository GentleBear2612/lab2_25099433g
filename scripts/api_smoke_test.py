import requests
import json

BASE = 'http://127.0.0.1:5001'

def pretty(r):
    try:
        return json.dumps(r.json(), ensure_ascii=False, indent=2)
    except Exception:
        return r.text

print('GET /api/notes')
r = requests.get(f'{BASE}/api/notes')
print(r.status_code, pretty(r))

print('\nPOST /api/notes (create)')
payload = {'title': 'api-smoke-title', 'content': 'api-smoke-content'}
r = requests.post(f'{BASE}/api/notes', json=payload)
print(r.status_code, pretty(r))
if r.status_code == 201:
    nid = r.json().get('id') or r.json().get('id')
    print('created id:', nid)
else:
    nid = None

if nid:
    print('\nPUT /api/notes/{}/ (update)'.format(nid))
    r2 = requests.put(f'{BASE}/api/notes/{nid}', json={'title': 'updated-title', 'content': 'updated-content'})
    print(r2.status_code, pretty(r2))

    print('\nPOST /api/notes/{}/translate (translate)'.format(nid))
    r3 = requests.post(f'{BASE}/api/notes/{nid}/translate', json={'to': 'English'})
    print(r3.status_code, pretty(r3))

    print('\nDELETE /api/notes/{} (delete)'.format(nid))
    r4 = requests.delete(f'{BASE}/api/notes/{nid}')
    print(r4.status_code, r4.text)

print('\nFinal GET /api/notes')
r = requests.get(f'{BASE}/api/notes')
print(r.status_code, pretty(r))
