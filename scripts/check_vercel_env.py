#!/usr/bin/env python3
"""
Script to check if the environment is properly configured for Vercel deployment.
"""
import os
import sys

def check_mongo_uri():
    """Check if MONGO_URI is set"""
    uri = os.environ.get('MONGODB_URI') or os.environ.get('MONGO_URI')
    if not uri:
        print("❌ MONGODB_URI / MONGO_URI environment variable is NOT set")
        print("   This will cause the application to use in-memory fallback storage")
        print("   Data will NOT be persisted across deployments")
        print("\n   To fix this:")
        print("   1. Go to your Vercel project settings")
        print("   2. Navigate to Environment Variables")
        print("   3. Add MONGODB_URI (or MONGO_URI) with your MongoDB connection string")
        return False
    else:
        print("✅ MONGODB_URI / MONGO_URI is set")
        # Check if it looks valid
        if uri.startswith('mongodb://') or uri.startswith('mongodb+srv://'):
            print(f"   URI format looks correct: {uri[:20]}...")
            return True
        else:
            print(f"⚠️  URI may be invalid. Expected to start with 'mongodb://' or 'mongodb+srv://'")
            print(f"   Current value: {uri[:50]}...")
            return False

def check_mongo_db_name():
    """Check if MONGO_DB_NAME is set"""
    db_name = os.environ.get('MONGO_DB_NAME', 'notetaker_db')
    print(f"✅ MONGO_DB_NAME is set to: {db_name}")
    if db_name == 'notetaker_db':
        print("   (using default value)")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import pymongo
        print("✅ pymongo is installed")
        print(f"   Version: {pymongo.__version__}")
    except ImportError:
        print("❌ pymongo is NOT installed")
        print("   Run: pip install pymongo")
        return False
    
    try:
        import certifi
        print("✅ certifi is installed")
    except ImportError:
        print("❌ certifi is NOT installed")
        print("   Run: pip install certifi")
        return False
    
    try:
        import flask
        print("✅ flask is installed")
        print(f"   Version: {flask.__version__}")
    except ImportError:
        print("❌ flask is NOT installed")
        print("   Run: pip install flask")
        return False
    
    return True

def test_mongo_connection():
    """Test MongoDB connection if URI is set"""
    uri = os.environ.get('MONGODB_URI') or os.environ.get('MONGO_URI')
    if not uri:
        print("\n⚠️  Skipping connection test (MONGODB_URI / MONGO_URI not set)")
        return False
    
    print("\n🔄 Testing MongoDB connection...")
    try:
        import pymongo
        import certifi
        
        client = pymongo.MongoClient(
            uri,
            serverSelectionTimeoutMS=5000,
            tlsCAFile=certifi.where()
        )
        
        # Test connection
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB!")
        
        # List databases
        db_list = client.list_database_names()
        print(f"   Available databases: {', '.join(db_list)}")
        
        return True
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {str(e)}")
        print("\n   Common issues:")
        print("   1. Check if password contains special characters (they need to be URL-encoded)")
        print("   2. Check MongoDB Atlas network access (whitelist 0.0.0.0/0 for Vercel)")
        print("   3. Verify the connection string format")
        return False

def main():
    print("=" * 60)
    print("Vercel Environment Configuration Check")
    print("=" * 60)
    print()
    
    checks = []
    
    print("Checking environment variables...")
    print("-" * 60)
    checks.append(check_mongo_uri())
    checks.append(check_mongo_db_name())
    print()
    
    print("Checking dependencies...")
    print("-" * 60)
    checks.append(check_dependencies())
    print()
    
    print("Testing connections...")
    print("-" * 60)
    checks.append(test_mongo_connection())
    print()
    
    print("=" * 60)
    if all(checks):
        print("✅ All checks passed! Your environment is ready for Vercel deployment.")
    else:
        print("⚠️  Some checks failed. Please review the issues above.")
        print("\nFor detailed setup instructions, see VERCEL_SETUP.md")
    print("=" * 60)

if __name__ == '__main__':
    main()
