#!/usr/bin/env python3
"""
Complete diagnostic tool for Vercel deployment issues.
Checks local setup, MongoDB connection, and simulates Vercel environment.
"""
import os
import sys
import json
import traceback

def check_environment_variables():
    """Check if required environment variables are set"""
    print("=" * 70)
    print("1. CHECKING ENVIRONMENT VARIABLES")
    print("=" * 70)
    
    mongo_uri = os.environ.get('MONGO_URI')
    mongo_db = os.environ.get('MONGO_DB_NAME', 'notetaker_db')
    
    if not mongo_uri:
        print("❌ CRITICAL: MONGO_URI is NOT set")
        print("\n🔧 FIX THIS IN VERCEL:")
        print("   1. Go to https://vercel.com/dashboard")
        print("   2. Select your project")
        print("   3. Settings → Environment Variables")
        print("   4. Add: MONGO_URI = your_mongodb_connection_string")
        print("   5. Make sure it's enabled for Production, Preview, Development")
        print("   6. Click Save")
        print("   7. Redeploy your application")
        return False
    else:
        print(f"✅ MONGO_URI is set: {mongo_uri[:30]}...")
        if not (mongo_uri.startswith('mongodb://') or mongo_uri.startswith('mongodb+srv://')):
            print("⚠️  WARNING: URI doesn't start with 'mongodb://' or 'mongodb+srv://'")
            return False
    
    print(f"✅ MONGO_DB_NAME: {mongo_db}")
    return True

def test_mongodb_connection():
    """Test MongoDB connection"""
    print("\n" + "=" * 70)
    print("2. TESTING MONGODB CONNECTION")
    print("=" * 70)
    
    try:
        import pymongo
        import certifi
        print("✅ pymongo and certifi packages are available")
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("   Run: pip install pymongo certifi")
        return False
    
    mongo_uri = os.environ.get('MONGO_URI')
    if not mongo_uri:
        print("⚠️  Skipping (MONGO_URI not set)")
        return False
    
    try:
        print("🔄 Connecting to MongoDB...")
        client = pymongo.MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=10000,
            tlsCAFile=certifi.where()
        )
        
        # Test connection
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB!")
        
        # Get database info
        db_name = os.environ.get('MONGO_DB_NAME', 'notetaker_db')
        db = client[db_name]
        
        # Check collections
        collections = db.list_collection_names()
        print(f"✅ Database: {db_name}")
        print(f"   Collections: {collections if collections else 'none'}")
        
        # Check notes count
        if 'notes' in collections:
            count = db.notes.count_documents({})
            print(f"   Notes in database: {count}")
            
            if count > 0:
                # Show a sample note
                sample = db.notes.find_one()
                print(f"   Sample note ID: {sample.get('_id')}")
        else:
            print("   ⚠️  'notes' collection doesn't exist yet (will be created on first insert)")
        
        return True
        
    except Exception as e:
        print(f"❌ MongoDB connection FAILED: {str(e)}")
        print("\n🔧 COMMON FIXES:")
        print("   1. Check MongoDB Atlas Network Access:")
        print("      - Go to https://cloud.mongodb.com")
        print("      - Network Access → Add IP Address")
        print("      - Add 0.0.0.0/0 (Allow from anywhere)")
        print("   2. Verify your connection string:")
        print("      - Username and password are correct")
        print("      - Special characters in password are URL-encoded")
        print("   3. Check if cluster is running (not paused)")
        traceback.print_exc()
        return False

def test_api_handler():
    """Test the API handler directly"""
    print("\n" + "=" * 70)
    print("3. TESTING API HANDLER (Simulating Vercel Function)")
    print("=" * 70)
    
    try:
        # Import the handler
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from api import notes
        
        print("✅ Successfully imported api.notes module")
        
        # Create mock request
        class MockRequest:
            method = 'GET'
            json = None
            args = {}
            url = 'http://localhost/api/notes'
            
            def get_json(self, silent=False):
                return self.json
        
        print("🔄 Calling notes.handler(request) with GET method...")
        request = MockRequest()
        response = notes.handler(request)
        
        # Check response type
        print(f"   Response type: {type(response).__name__}")
        
        if hasattr(response, 'status_code'):
            print(f"   Status code: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Handler returned 200 OK")
                
                # Get response data
                data = response.get_data(as_text=True)
                try:
                    json_data = json.loads(data)
                    print(f"✅ Response is valid JSON")
                    print(f"   Type: {type(json_data).__name__}")
                    if isinstance(json_data, list):
                        print(f"   Contains {len(json_data)} notes")
                        if len(json_data) > 0:
                            print(f"   First note: {json_data[0].get('title', 'N/A')[:50]}")
                    return True
                except json.JSONDecodeError as e:
                    print(f"❌ Response is not valid JSON: {e}")
                    print(f"   Response preview: {data[:200]}")
                    return False
            elif response.status_code == 503:
                print("❌ Handler returned 503 Service Unavailable")
                print("   This means MONGO_URI is not configured properly")
                data = response.get_data(as_text=True)
                print(f"   Error: {data}")
                return False
            else:
                print(f"❌ Handler returned unexpected status: {response.status_code}")
                data = response.get_data(as_text=True)
                print(f"   Response: {data[:500]}")
                return False
        else:
            print(f"⚠️  Response is not a Flask Response object: {type(response)}")
            print(f"   Response: {response}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API handler: {str(e)}")
        traceback.print_exc()
        return False

def check_flask_import():
    """Verify Flask is available"""
    print("\n" + "=" * 70)
    print("4. CHECKING FLASK AVAILABILITY")
    print("=" * 70)
    
    try:
        import flask
        print(f"✅ Flask is installed (version {flask.__version__})")
        
        from flask import Response
        print("✅ Flask Response is available")
        
        # Test creating a response
        resp = Response(json.dumps({"test": "data"}), status=200, mimetype='application/json')
        print(f"✅ Can create Flask Response objects")
        print(f"   Test response status: {resp.status_code}")
        
        return True
    except ImportError as e:
        print(f"❌ Flask import error: {e}")
        print("   Run: pip install flask")
        return False

def print_vercel_instructions():
    """Print final instructions for Vercel"""
    print("\n" + "=" * 70)
    print("5. VERCEL DEPLOYMENT CHECKLIST")
    print("=" * 70)
    
    print("""
If tests above passed locally but Vercel still shows 500 errors:

📋 VERCEL DASHBOARD CHECKLIST:
   
   Step 1: Verify Environment Variables
   -------------------------------------
   □ Go to: https://vercel.com/dashboard
   □ Select your project
   □ Go to: Settings → Environment Variables
   □ Verify MONGO_URI exists and is correct
   □ Verify it's enabled for: Production ✓ Preview ✓ Development ✓
   □ Click "Save" if you made any changes
   
   Step 2: Verify MongoDB Atlas
   -----------------------------
   □ Go to: https://cloud.mongodb.com
   □ Select your cluster
   □ Go to: Network Access
   □ Verify 0.0.0.0/0 is in the IP Access List
   □ Verify your database user credentials are correct
   
   Step 3: Redeploy
   ----------------
   □ Go back to Vercel Dashboard
   □ Go to: Deployments tab
   □ Click on the latest deployment
   □ Click the "..." menu → "Redeploy"
   □ Wait for deployment to complete
   
   Step 4: Check Function Logs
   ----------------------------
   □ After redeployment, visit your site
   □ Trigger the error (visit /api/notes)
   □ Go to: Vercel Dashboard → Deployments → Latest
   □ Click "Functions" tab
   □ Click on "/api/notes"
   □ Read the error logs
   
   Step 5: Test the API Directly
   ------------------------------
   □ Open: https://your-app.vercel.app/api/notes
   □ Should return: [] (empty array) or array of notes
   □ Should NOT return: 500 error

🔍 DEBUGGING TIPS:

   If you see "MONGO_URI not set" in Vercel logs:
   → Environment variable not configured properly
   → Make sure to redeploy after adding env vars
   
   If you see "Unable to connect to MongoDB":
   → Check MongoDB Atlas Network Access (0.0.0.0/0)
   → Verify connection string format
   → Check if cluster is paused
   
   If you see "Authentication failed":
   → Password may contain special characters
   → URL-encode special characters in password:
     @ → %40, ! → %21, # → %23, etc.

📞 NEED MORE HELP?
   
   Review these files in your repository:
   - FIX_SUMMARY.md (complete fix guide)
   - VERCEL_SETUP.md (detailed setup)
   - CHECKLIST.md (step-by-step checklist)
""")

def main():
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "VERCEL DEPLOYMENT DIAGNOSTIC TOOL" + " " * 20 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    results = []
    
    # Run all checks
    results.append(("Environment Variables", check_environment_variables()))
    results.append(("MongoDB Connection", test_mongodb_connection()))
    results.append(("Flask Import", check_flask_import()))
    results.append(("API Handler", test_api_handler()))
    
    # Print Vercel instructions
    print_vercel_instructions()
    
    # Summary
    print("\n" + "=" * 70)
    print("DIAGNOSTIC SUMMARY")
    print("=" * 70)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✅ ALL LOCAL CHECKS PASSED!")
        print("\nIf Vercel still shows 500 errors, the issue is in Vercel configuration.")
        print("Follow the VERCEL DEPLOYMENT CHECKLIST above.")
    else:
        print("❌ SOME CHECKS FAILED")
        print("\nFix the failed checks above before deploying to Vercel.")
        print("Most likely issue: MONGO_URI environment variable not set")
    print("=" * 70)
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    raise SystemExit(main())
