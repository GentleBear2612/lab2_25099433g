import ssl
import socket
import sys
from time import perf_counter
hosts = [
    'ac-cktidfe-shard-00-00.kskvhe8.mongodb.net',
    'ac-cktidfe-shard-00-01.kskvhe8.mongodb.net',
    'ac-cktidfe-shard-00-02.kskvhe8.mongodb.net',
]
print('Python:', sys.version.replace('\n',' '))
print('OpenSSL:', getattr(ssl, 'OPENSSL_VERSION', 'unknown'))
print('HAS_SNI:', getattr(ssl, 'HAS_SNI', False))
print('')
ctx = ssl.create_default_context()
for h in hosts:
    print('Host:', h)
    start = perf_counter()
    try:
        sock = socket.create_connection((h, 27017), timeout=5)
        try:
            ss = ctx.wrap_socket(sock, server_hostname=h)
            cipher = ss.cipher()
            elapsed = perf_counter() - start
            print('  TLS OK, cipher:', cipher, f'({elapsed:.2f}s)')
            ss.close()
        except Exception as e:
            elapsed = perf_counter() - start
            print('  TLS handshake FAILED:', type(e).__name__, str(e), f'({elapsed:.2f}s)')
            try:
                sock.close()
            except Exception:
                pass
    except Exception as e:
        elapsed = perf_counter() - start
        print('  TCP connect FAILED:', type(e).__name__, str(e), f'({elapsed:.2f}s)')
    print('')
print('Done')
