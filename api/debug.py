"""
超级简化版本 - 只测试 Flask 能否启动
完全不依赖任何自定义代码
"""
from flask import Flask, jsonify
import os
import sys

app = Flask(__name__)

@app.route('/api/debug', methods=['GET'])
def debug():
    """显示所有环境信息"""
    return jsonify({
        'status': 'ok',
        'message': 'Flask is working!',
        'python_version': sys.version,
        'python_path': sys.path[:5],
        'cwd': os.getcwd(),
        'env_vars': {
            'VERCEL': os.environ.get('VERCEL'),
            'MONGODB_URI_SET': bool(os.environ.get('MONGODB_URI')),
            'MONGO_DB_NAME': os.environ.get('MONGO_DB_NAME', 'not set')
        },
        'files_in_current_dir': os.listdir('.')[:20]
    })

@app.route('/api/health', methods=['GET'])
def health():
    """基本健康检查"""
    return jsonify({
        'status': 'ok',
        'message': 'Super minimal Flask app is working!'
    })

# Vercel 需要这个
app = app
