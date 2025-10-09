"""
最小化测试版本 - 用于诊断 Vercel 部署问题
如果这个能工作，说明问题在 src/main.py 的导入或配置中
"""
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({
        'status': 'ok',
        'message': 'Minimal Flask app is working!',
        'environment': 'vercel'
    })

@app.route('/api/health', methods=['GET'])
def health():
    import os
    return jsonify({
        'status': 'ok',
        'message': 'Health check passed',
        'mongodb_uri_set': bool(os.environ.get('MONGODB_URI')),
        'python_version': os.sys.version
    })

if __name__ == '__main__':
    app.run(debug=True)
