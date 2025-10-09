"""
Vercel serverless function - 健康检查端点
单独的文件，单独的端点
"""
from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
@app.route('/api/health', methods=['GET'])
def health():
    """健康检查端点"""
    return jsonify({
        'status': 'ok',
        'message': 'Health check endpoint is working',
        'mongodb_uri_set': bool(os.environ.get('MONGODB_URI')),
        'service': 'NoteTaker API'
    })
