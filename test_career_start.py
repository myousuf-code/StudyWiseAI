#!/usr/bin/env python3
"""
Test script for career counseling start endpoint
"""
import requests
import json

def test_career_counseling():
    base_url = "http://localhost:8000"
    
    # Register and login
    print("Creating test user...")
    
    # Register test user
    try:
        reg_response = requests.post(
            f"{base_url}/api/auth/register",
            json={
                "email": "testcareer@example.com",
                "username": "testcareer",
                "password": "testpass123",
                "full_name": "Test Career User"
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
                "username": "testcareer@example.com",  # Use email as username
                "password": "testpass123"
            }
        )
        print(f"Login status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            token = token_data["access_token"]
            print("✅ Got authentication token!")
            
            # Test career counseling start
            print("\nTesting career counseling start...")
            headers = {"Authorization": f"Bearer {token}"}
            
            # Add timeout to the request
            import time
            start_time = time.time()
            
            try:
                response = requests.post(
                    f"{base_url}/api/ai/career-counseling/start",
                    headers=headers,
                    json={"target_profession": "Software Engineer"},
                    timeout=60  # 60 second timeout
                )
                elapsed = time.time() - start_time
                print(f"Request completed in {elapsed:.2f} seconds")
                print(f"Status: {response.status_code}")
                print(f"Response: {response.text}")
                
                if response.status_code == 500:
                    print("❌ 500 error occurred!")
                    return response.text
                elif response.status_code == 504:
                    print("⏱️ Timeout error - AI model too slow")
                    return response.text
                else:
                    print("✅ Career counseling endpoint working!")
                    
            except requests.exceptions.Timeout:
                elapsed = time.time() - start_time
                print(f"⏱️ Request timed out after {elapsed:.2f} seconds")
                print("❌ Frontend timeout - try increasing timeout settings")
            except Exception as e:
                elapsed = time.time() - start_time
                print(f"❌ Request failed after {elapsed:.2f} seconds: {e}")
                
        else:
            print("❌ Could not get auth token")
            print(f"Login response: {login_response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_career_counseling()