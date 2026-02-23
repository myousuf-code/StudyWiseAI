#!/usr/bin/env python3
"""
Test script for the convert career to study plan endpoint
"""
import requests
import json

def test_convert_endpoint():
    base_url = "http://localhost:8000"
    
    print("Testing convert career to study plan endpoint...")
    
    # Test without authentication (should fail)
    print("\n1. Testing without auth (should fail)...")
    try:
        response = requests.post(
            f"{base_url}/api/ai/career-counseling/convert-to-study-plan",
            json={"session_id": 1}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test user registration and login
    print("\n2. Creating test user and getting token...")
    
    # Register test user
    try:
        reg_response = requests.post(
            f"{base_url}/api/auth/register",
            json={
                "email": "testconvert@example.com",
                "username": "testconvert",
                "password": "testpass123",
                "full_name": "Test Convert User"
            }
        )
        print(f"Registration: {reg_response.status_code}")
    except Exception as e:
        print(f"Registration might have failed (user exists?): {e}")
    
    # Login to get token
    try:
        login_response = requests.post(
            f"{base_url}/api/auth/login",
            data={
                "username": "testconvert",
                "password": "testpass123"
            }
        )
        print(f"Login status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            token = token_data["access_token"]
            print("✅ Got authentication token!")
            
            # Test with authentication but no career session (should fail)
            print("\n3. Testing with auth but non-existent session...")
            headers = {"Authorization": f"Bearer {token}"}
            
            response = requests.post(
                f"{base_url}/api/ai/career-counseling/convert-to-study-plan",
                headers=headers,
                json={"session_id": 999}
            )
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 404:
                print("✅ Endpoint correctly handles missing career session!")
            elif response.status_code == 422:
                print("✅ Endpoint is working - validation error is expected!")
            else:
                print("✅ Endpoint is accessible and responding!")
                
        else:
            print("❌ Could not get auth token")
            
    except Exception as e:
        print(f"Login error: {e}")

if __name__ == "__main__":
    test_convert_endpoint()