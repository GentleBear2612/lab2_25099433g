from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    """Vercel HTTP handler format"""
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Hello from BaseHTTPRequestHandler!')
        return
