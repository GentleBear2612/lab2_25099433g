#!/usr/bin/env python3
"""
Emergency script to test what Vercel actually sees.
This simulates the exact Vercel environment.
"""
import os
import sys

# Set up path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("=" * 70)
print("SIMULATING VERCEL SERVERLESS FUNCTION ENVIRONMENT")
print("=" * 70)
print()

# Test 1: Import the module
print("1️⃣ Testing module import...")
try:
    from api import notes
    print("✅ Successfully imported api.notes")
except Exception as e:
    print(f"❌ Failed to import: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: Check if handler exists
print("\n2️⃣ Checking handler function...")
if hasattr(notes, 'handler'):
    print("✅ handler function exists")
else:
    print("❌ handler function not found")
    sys.exit(1)

# Test 3: Create a mock Vercel request
print("\n3️⃣ Creating mock Vercel request...")

class VercelRequest:
    """Mock Vercel serverless function request object"""
    def __init__(self):
        self.method = 'GET'
        self.args = {}
        self.json = None
        self.url = 'https://your-app.vercel.app/api/notes'
        self.headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        }
    
    def get_json(self, silent=False):
        return self.json

request = VercelRequest()
print(f"✅ Mock request created: {request.method} {request.url}")

# Test 4: Call the handler
print("\n4️⃣ Calling notes.handler(request)...")
print("-" * 70)

try:
    response = notes.handler(request)
    print(f"\n✅ Handler executed successfully")
    print(f"Response type: {type(response).__name__}")
    
    # Check if it's a Flask Response
    if hasattr(response, 'status_code'):
        print(f"Status code: {response.status_code}")
        print(f"Content-Type: {response.content_type}")
        
        # Get the body
        body = response.get_data(as_text=True)
        print(f"\nResponse body length: {len(body)} bytes")
        print(f"Response body preview (first 500 chars):")
        print("-" * 70)
        print(body[:500])
        print("-" * 70)
        
        # Try to parse as JSON
        if response.status_code == 200:
            import json
            try:
                data = json.loads(body)
                print(f"\n✅ Valid JSON response")
                print(f"Data type: {type(data).__name__}")
                if isinstance(data, list):
                    print(f"Number of items: {len(data)}")
            except json.JSONDecodeError as e:
                print(f"\n❌ Invalid JSON: {e}")
        elif response.status_code == 503:
            print("\n⚠️ Service Unavailable (503)")
            print("This means MONGO_URI is not set or connection failed")
        elif response.status_code == 500:
            print("\n❌ Internal Server Error (500)")
            print("There's an error in the handler code")
            
    else:
        print(f"\n⚠️ Response is not a Flask Response object")
        print(f"Response: {response}")
        
except Exception as e:
    print(f"\n❌ Handler raised an exception:")
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {str(e)}")
    print("\nFull traceback:")
    print("-" * 70)
    import traceback
    traceback.print_exc()
    print("-" * 70)

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)

# Test 5: Check what Vercel would actually return
print("\n5️⃣ Checking Vercel response format...")

try:
    response = notes.handler(request)
    
    # Vercel expects either:
    # 1. A Flask Response object (what we're returning)
    # 2. A tuple (response_body, status_code, headers)
    # 3. A WSGI-compatible response
    
    if hasattr(response, '__call__'):
        print("✅ Response is callable (WSGI-compatible)")
    elif hasattr(response, 'status_code'):
        print("✅ Response is a Flask Response object")
        print(f"   This is correct for Vercel's @vercel/python runtime")
    elif isinstance(response, tuple):
        print("⚠️ Response is a tuple")
        print(f"   Length: {len(response)}")
    elif isinstance(response, dict):
        print("❌ Response is a dict (old AWS Lambda format)")
        print("   This won't work with Vercel!")
    else:
        print(f"⚠️ Unknown response type: {type(response)}")
    
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 70)
print("If everything above passes but Vercel still fails,")
print("the issue is likely in Vercel's environment configuration.")
print("=" * 70)
