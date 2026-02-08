#!/usr/bin/env python3
"""
Simple test script to verify authentication is working
"""
import requests
import json
import random

def test_registration():
    """Test user registration endpoint"""
    url = "http://localhost:8000/api/auth/register"
    
    test_user = {
        "email": f"test{random.randint(1000,9999)}@example.com",
        "username": f"testuser{random.randint(1000,9999)}",
        "password": "test123456",
        "full_name": "Test User"
    }
    
    try:
        response = requests.post(url, json=test_user)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Registration successful!")
            return response.json()
        else:
            print(f"❌ Registration failed: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Is it running?")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_server_health():
    """Test if server is responding"""
    try:
        response = requests.get("http://localhost:8000/")
        print(f"Server health check - Status: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"Server not responding: {e}")
        return False

if __name__ == "__main__":
    print("Testing StudyWiseAI Authentication...")
    print("=" * 40)
    
    # Test server health first
    if test_server_health():
        print("Server is responding!")
        print("\nTesting registration...")
        result = test_registration()
    else:
        print("Server is not responding!")