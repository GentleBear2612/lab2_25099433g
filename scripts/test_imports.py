modules = ['api._mongo','api.notes','api.note','api.users','api.user']
for m in modules:
    try:
        __import__(m)
        print('OK import', m)
    except Exception as e:
        print('IMPORT FAILED', m, type(e).__name__, e)
