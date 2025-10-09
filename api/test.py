# Vercel Python 函数测试
# 参考: https://vercel.com/docs/functions/runtimes/python

# 方式 1: 使用 http.server.BaseHTTPRequestHandler
from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            'status': 'ok',
            'message': 'Vercel Python function is working!',
            'format': 'BaseHTTPRequestHandler'
        }
        
        self.wfile.write(json.dumps(response).encode())
        return
