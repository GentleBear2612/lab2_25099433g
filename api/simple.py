"""
终极简化版本 - 只测试 Vercel Python 运行时能否工作
不依赖任何第三方库
"""

def handler(event, context):
    """最简单的 Vercel handler"""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': '{"status": "ok", "message": "Vercel Python runtime is working!", "test": "ultra-minimal"}'
    }

# 也尝试 WSGI 接口
def application(environ, start_response):
    """WSGI 接口"""
    status = '200 OK'
    response_headers = [('Content-Type', 'application/json')]
    start_response(status, response_headers)
    return [b'{"status": "ok", "message": "WSGI is working!"}']

# Flask 版本
try:
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/api/simple')
    @app.route('/simple')
    @app.route('/')
    def simple():
        return jsonify({
            'status': 'ok',
            'message': 'Ultra simple Flask is working!',
            'version': 'v1'
        })
    
    # 导出 Flask app
    app = app
except Exception as e:
    # 如果 Flask 导入失败，使用纯 Python handler
    import sys
    sys.stderr.write(f"Failed to import Flask: {e}\n")
    app = None
