import os
os.environ.pop('MONGO_URI', None)
from api import notes

class Req:
    def __init__(self, method, json_body=None):
        self.method = method
        self._json = json_body
    @property
    def json(self):
        return self._json
    def get_json(self, silent=True):
        return self._json
    @property
    def body(self):
        import json
        return json.dumps(self._json).encode('utf-8') if self._json is not None else b''

req = Req('POST', {'title':'Test', 'content':'This is a test'})
res = notes.handler(req)
print(res)
