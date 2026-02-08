#!/usr/bin/env python3
"""
Debug Database and Try Fresh Credentials
"""
import requests
import json
import random

def test_with_fresh_credentials():
    """Test with completely fresh credentials"""
    print("🆕 Testing with FRESH credentials...")
    
    # Generate unique credentials
    user_id = random.randint(1000, 9999)
    user_data = {
        "email": f"fresh{user_id}@example.com",
        "username": f"fresh{user_id}",
        "password": "freshpass123",
        "full_name": "Fresh Test User"
    }
    
    print(f"Using credentials:")
    print(f"  Email: {user_data['email']}")
    print(f"  Username: {user_data['username']}")
    print(f"  Password: {user_data['password']}")
    
    # Register
    try:
        print("\n📝 Registering fresh user...")
        response = requests.post("http://localhost:8000/api/auth/register", 
                               json=user_data, 
                               timeout=10)
        
        print(f"Registration Status: {response.status_code}")
        if response.status_code != 200:
            print(f"❌ Registration failed: {response.text}")
            return False
        print("✅ Registration successful!")
        
        # Try login with email
        print("\n🔑 Testing login with EMAIL...")
        login_data = {
            "username": user_data["email"],  # Using email as username
            "password": user_data["password"]
        }
        
        response = requests.post("http://localhost:8000/api/auth/login", 
                               data=login_data,
                               timeout=10)
        
        print(f"Login Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ LOGIN WORKS! The issue was stale credentials.")
            data = response.json()
            print(f"Token received: {data.get('access_token', '')[:20]}...")
            return True
        else:
            print(f"❌ Login still failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_existing_user():
    """Check what's wrong with the existing test@example.com user"""
    print("🔍 Checking existing user issue...")
    
    # Try to understand what's in the database
    from fastapi.testclient import TestClient
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        from app.main import app
        from app.core.database import SessionLocal
        from app.models.database import User
        
        client = TestClient(app)
        db = SessionLocal()
        
        # Find the problematic user
        user = db.query(User).filter(User.email == "test@example.com").first()
        if user:
            print(f"✅ Found user in database:")
            print(f"  ID: {user.id}")
            print(f"  Email: {user.email}")  
            print(f"  Username: {user.username}")
            print(f"  Active: {user.is_active}")
            print(f"  Password Hash: {user.hashed_password[:20]}...")
            
            # Test password verification directly
            from app.core.auth import verify_password
            is_valid = verify_password("mypassword123", user.hashed_password)
            print(f"  Password 'mypassword123' valid: {is_valid}")
            
            if not is_valid:
                print("🔧 PASSWORD MISMATCH! This is the issue.")
                return False
            else:
                print("✅ Password is valid, issue is elsewhere")
                return True
        else:
            print("❌ User not found in database")
            return False
            
        db.close()
        
    except Exception as e:
        print(f"❌ Database check error: {e}")
        return False

def main():
    print("🔧 DEBUG: Login Issue Analysis")
    print("=" * 40)
    
    # First try fresh credentials to see if auth system works
    fresh_works = test_with_fresh_credentials()
    
    if fresh_works:
        print(f"\n✅ SOLUTION FOUND!")
        print(f"The authentication system works fine.")
        print(f"The issue is with the existing 'test@example.com' user.")
        print(f"\n🎯 TO FIX TEST 1.3:")
        print(f"Either:")
        print(f"1. Use fresh credentials instead")
        print(f"2. Or reset the database: rm studywiseai.db")
        print(f"3. Or check what's wrong with the existing user")
        
        # Check existing user issue
        print(f"\n" + "="*40)
        check_existing_user()
        
    else:
        print(f"\n❌ AUTHENTICATION SYSTEM ISSUE")
        print(f"Even fresh credentials don't work.")
        print(f"Check the server logs for errors.")

if __name__ == "__main__":
    main()