#!/usr/bin/env python3
"""
Simple test script to check what's failing during import
"""
import os
import sys

def test_imports():
    print("=== Testing imports ===")
    
    try:
        print("1. Testing basic FastAPI import...")
        import fastapi
        print("✅ FastAPI imported")
    except Exception as e:
        print(f"❌ FastAPI failed: {e}")
        return False
    
    try:
        print("2. Testing SQLAlchemy import...")
        import sqlalchemy
        print("✅ SQLAlchemy imported")
    except Exception as e:
        print(f"❌ SQLAlchemy failed: {e}")
        return False
    
    try:
        print("3. Testing app.db import...")
        from app.db import Base, engine
        print("✅ app.db imported")
    except Exception as e:
        print(f"❌ app.db failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    try:
        print("4. Testing app.main import...")
        from app.main import app
        print("✅ app.main imported")
        return True
    except Exception as e:
        print(f"❌ app.main failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print(f"Working directory: {os.getcwd()}")
    print(f"DATABASE_URL: {os.environ.get('DATABASE_URL', 'NOT SET')}")
    
    if test_imports():
        print("\n🎉 All imports successful!")
    else:
        print("\n💥 Import test failed!")
        sys.exit(1)
