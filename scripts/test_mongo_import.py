from api._mongo import get_client

if __name__ == '__main__':
    try:
        get_client()
        print('ERROR: expected RuntimeError when MONGO_URI not set')
    except RuntimeError as e:
        print('OK: RuntimeError as expected:', e)
    except Exception as e:
        print('Unexpected exception:', type(e).__name__, e)
