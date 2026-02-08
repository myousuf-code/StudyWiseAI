#!/usr/bin/env python3
"""
Direct FastAPI test to diagnose endpoint issues
"""
import os
import sys
import random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from app.main import app
from app.core.database import create_tables

# Create test client
client = TestClient(app)

def test_registration_endpoint():
    """Test the registration endpoint directly using FastAPI TestClient"""
    print("Testing registration endpoint with TestClient...")
    
    # Ensure database is initialized
    create_tables()
    
    import random
    test_user = {
        "email": f"directtest{random.randint(1000,9999)}@example.com",
        "username": f"directtest{random.randint(1000,9999)}",
        "password": "test123456",
        "full_name": "Direct Test User"
    }
    
    try:
        print(f"Sending registration request for: {test_user['email']}")
        response = client.post("/api/auth/register", json=test_user)
        print(f"Response Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Content: {response.text}")
        
        if response.status_code == 200:
            print("✅ Registration successful!")
            return response.json()
        else:
            print(f"❌ Registration failed with status {response.status_code}")
            print(f"Detail: {response.text}")
            return None
    
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_root_endpoint():
    """Test the root endpoint"""
    try:
        response = client.get("/")
        print(f"Root endpoint status: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"Root endpoint failed: {e}")
        return False

if __name__ == "__main__":
    print("Direct FastAPI Endpoint Test")
    print("=" * 35)
    
    # Test root endpoint first
    root_works = test_root_endpoint()
    
    if root_works:
        print("✅ Root endpoint works")
        print("\nTesting registration endpoint...")
        result = test_registration_endpoint()
    else:
        print("❌ Root endpoint failed, skipping registration test")