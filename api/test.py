"""
Ultra-minimal test handler for Vercel debugging
This version has zero dependencies to isolate the issue
"""
import json
from datetime import datetime


def handler(request):
    """Absolute minimal handler for debugging"""
    try:
        # Just return a simple response - no MongoDB, no imports
        result = {
            "status": "ok",
            "message": "Handler is working",
            "timestamp": datetime.utcnow().isoformat(),
            "method": getattr(request, 'method', 'UNKNOWN'),
            "test_data": [
                {"id": "1", "title": "Test 1"},
                {"id": "2", "title": "Test 2"}
            ]
        }
        
        # Try to create response
        try:
            from flask import Response
            return Response(
                json.dumps(result),
                status=200,
                mimetype='application/json',
                headers={'Access-Control-Allow-Origin': '*'}
            )
        except ImportError as e:
            # If Flask import fails, return dict format
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(result)
            }
            
    except Exception as e:
        import traceback
        import sys
        
        error_detail = {
            'error': str(e),
            'type': type(e).__name__,
            'traceback': traceback.format_exc()
        }
        
        # Print to stderr for Vercel logs
        print(f"ERROR: {error_detail}", file=sys.stderr)
        
        try:
            from flask import Response
            return Response(
                json.dumps(error_detail),
                status=500,
                mimetype='application/json'
            )
        except:
            return {
                'statusCode': 500,
                'body': json.dumps(error_detail)
            }


# Multiple entry points for maximum compatibility
def main(request):
    return handler(request)

def index(request):
    return handler(request)

# WSGI application interface
def application(environ, start_response):
    """WSGI interface"""
    try:
        from flask import Flask, request
        app = Flask(__name__)
        
        with app.test_request_context(environ):
            response = handler(request)
            return response(environ, start_response)
    except Exception as e:
        start_response('500 Internal Server Error', [('Content-Type', 'application/json')])
        return [json.dumps({'error': str(e)}).encode()]
