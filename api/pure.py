"""
绝对最小化 - 不使用任何第三方库
只使用 Python 标准库
"""

def handler(request):
    """Vercel serverless function handler"""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain',
        },
        'body': 'Hello from pure Python! No Flask, no nothing.'
    }

# 如果 Vercel 期望的是其他接口
def application(environ, start_response):
    """WSGI application"""
    status = '200 OK'
    response_headers = [('Content-Type', 'text/plain')]
    start_response(status, response_headers)
    return [b'Hello from WSGI!']

# 如果 Vercel 期望的是模块级别的变量
def app(environ, start_response):
    """Another WSGI interface"""
    status = '200 OK'
    response_headers = [('Content-Type', 'text/plain')]
    start_response(status, response_headers)
    return [b'Hello from app WSGI!']
