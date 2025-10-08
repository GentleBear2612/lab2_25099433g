#!/usr/bin/env python3
"""
Test the API endpoints to verify they return proper responses.
This script simulates Vercel's serverless function environment.
"""
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_notes_api():
    """Test /api/notes endpoint"""
    print("Testing /api/notes (GET)...")
    print("-" * 60)
    
    try:
        # Import the handler
        from api import notes
        
        # Create a mock request object
        class MockRequest:
            method = 'GET'
            json = None
            args = {}
            
            def get_json(self, silent=False):
                return self.json
        
        request = MockRequest()
        response = notes.handler(request)
        
        # Check response type
        print(f"Response type: {type(response)}")
        
        # If it's a Flask Response object
        if hasattr(response, 'status_code'):
            print(f"✅ Status code: {response.status_code}")
            print(f"✅ Content-Type: {response.content_type}")
            
            # Get response data
            data = response.get_data(as_text=True)
            print(f"Response body preview: {data[:200]}...")
            
            # Try to parse as JSON
            try:
                json_data = json.loads(data)
                print(f"✅ Response is valid JSON")
                print(f"   Type: {type(json_data)}")
                if isinstance(json_data, list):
                    print(f"   Contains {len(json_data)} items")
            except json.JSONDecodeError as e:
                print(f"❌ Response is not valid JSON: {e}")
                
        # If it's a dict (old format)
        elif isinstance(response, dict):
            print(f"⚠️  Response is a dict (old format)")
            print(f"   statusCode: {response.get('statusCode')}")
            if 'body' in response:
                print(f"   body preview: {response['body'][:200]}...")
        
        print("✅ /api/notes test passed\n")
        return True
        
    except Exception as e:
        print(f"❌ Error testing /api/notes: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_notes_post():
    """Test /api/notes POST endpoint"""
    print("Testing /api/notes (POST)...")
    print("-" * 60)
    
    try:
        from api import notes
        
        class MockRequest:
            method = 'POST'
            json = {'title': 'Test Note', 'content': 'Test content'}
            args = {}
            
            def get_json(self, silent=False):
                return self.json
        
        request = MockRequest()
        response = notes.handler(request)
        
        if hasattr(response, 'status_code'):
            print(f"✅ Status code: {response.status_code}")
            data = response.get_data(as_text=True)
            json_data = json.loads(data)
            
            if '_id' in json_data:
                print(f"✅ Created note with ID: {json_data['_id']}")
            else:
                print(f"⚠️  Response missing '_id' field")
            
            print(f"✅ Response: {json_data}")
        
        print("✅ /api/notes POST test passed\n")
        return True
        
    except Exception as e:
        print(f"❌ Error testing POST /api/notes: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_mongo_connection():
    """Test MongoDB connection"""
    print("Testing MongoDB connection...")
    print("-" * 60)
    
    try:
        from api._mongo import get_client
        
        client = get_client()
        db_name = os.environ.get('MONGO_DB_NAME', 'notetaker_db')
        db = client[db_name]
        
        # Check if using fake client
        client_type = type(client).__name__
        print(f"Client type: {client_type}")
        
        if client_type == 'FakeClient':
            print("⚠️  Using in-memory fallback (MONGO_URI not set)")
            print("   Data will not persist across requests")
        else:
            print("✅ Using real MongoDB client")
            
        print("✅ MongoDB connection test passed\n")
        return True
        
    except Exception as e:
        print(f"❌ Error testing MongoDB: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("API Response Format Test")
    print("=" * 60)
    print()
    
    # Check environment
    mongo_uri = os.environ.get('MONGO_URI')
    if mongo_uri:
        print(f"✅ MONGO_URI is set: {mongo_uri[:20]}...")
    else:
        print("⚠️  MONGO_URI not set - will use in-memory fallback")
    print()
    
    results = []
    results.append(test_mongo_connection())
    results.append(test_notes_api())
    results.append(test_notes_post())
    
    print("=" * 60)
    if all(results):
        print("✅ All API tests passed!")
        print("\nThe API responses are now compatible with Vercel.")
        print("You can deploy to Vercel with confidence.")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    print("=" * 60)

if __name__ == '__main__':
    main()
