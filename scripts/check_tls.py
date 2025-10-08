import ssl
import socket
import traceback

hosts = [
    'ac-cktidfe-shard-00-00.kskvhe8.mongodb.net',
    'ac-cktidfe-shard-00-01.kskvhe8.mongodb.net',
    'ac-cktidfe-shard-00-02.kskvhe8.mongodb.net'
]
port = 27017

print('Python:', __import__('sys').version)
print('OpenSSL:', getattr(ssl, 'OPENSSL_VERSION', 'unknown'))
print('HAS_SNI:', getattr(ssl, 'HAS_SNI', False))
print('Default verify locations:')
try:
    ctx = ssl.create_default_context()
    vs = ctx.get_ca_certs()
    print('  CA certs count (may be 0 on Windows):', len(vs))
except Exception as e:
    print('  error getting CA certs:', e)

for h in hosts:
    print('\nTesting host:', h)
    try:
        s = socket.create_connection((h, port), timeout=5)
    except Exception:
        print('  TCP connect failed:')
        traceback.print_exc()
        continue
    try:
        ctx = ssl.create_default_context()
        # require TLS and hostname check
        ctx.check_hostname = True
        ctx.verify_mode = ssl.CERT_REQUIRED
        ss = ctx.wrap_socket(s, server_hostname=h)
        print('  TLS OK, cipher:', ss.cipher())
        ss.close()
    except Exception:
        print('  TLS handshake failed:')
        traceback.print_exc()
    finally:
        try:
            s.close()
        except Exception:
            pass
