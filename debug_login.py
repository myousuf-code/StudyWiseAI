#!/usr/bin/env python3
"""
Debug Test 1.3 Login Issue
Tests the exact credentials from TEST_PLAN.md to see why login is failing
"""
import requests
import json

def test_registration():
    """Test registration with exact credentials from Test 1.3"""
    print("🔐 Testing Registration (Test 1.3 credentials)...")
    
    # Exact credentials from TEST_PLAN.md
    user_data = {
        "email": "test@example.com",
        "username": "testuser123", 
        "password": "mypassword123",
        "full_name": "Test User"
    }
    
    try:
        response = requests.post("http://localhost:8000/api/auth/register", 
                               json=user_data, 
                               timeout=10)
        
        print(f"Registration Status: {response.status_code}")
        print(f"Registration Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Registration successful!")
            return True
        else:
            print(f"❌ Registration failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return False

def test_login_with_email():
    """Test login using EMAIL (as shown in frontend JavaScript)"""
    print("\n🔑 Testing Login with EMAIL...")
    
    # Login data using EMAIL (as the frontend JavaScript does)
    login_data = {
        "username": "test@example.com",  # Frontend sends email as username
        "password": "mypassword123"
    }
    
    try:
        response = requests.post("http://localhost:8000/api/auth/login", 
                               data=login_data,  # OAuth2 uses form data, not JSON
                               timeout=10)
        
        print(f"Email Login Status: {response.status_code}")
        print(f"Email Login Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Email login successful!")
            data = response.json()
            print(f"Token received: {data.get('access_token', 'No token')[:20]}...")
            return True
        else:
            print(f"❌ Email login failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Email login error: {e}")
        return False

def test_login_with_username():
    """Test login using USERNAME"""
    print("\n🔑 Testing Login with USERNAME...")
    
    # Login data using actual USERNAME
    login_data = {
        "username": "testuser123",  # Actual username
        "password": "mypassword123"
    }
    
    try:
        response = requests.post("http://localhost:8000/api/auth/login", 
                               data=login_data,
                               timeout=10)
        
        print(f"Username Login Status: {response.status_code}")
        print(f"Username Login Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Username login successful!")
            data = response.json()
            print(f"Token received: {data.get('access_token', 'No token')[:20]}...")
            return True
        else:
            print(f"❌ Username login failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Username login error: {e}")
        return False

def test_website_accessibility():
    """Test if website is accessible"""
    print("\n🌐 Testing Website Accessibility...")
    
    try:
        response = requests.get("http://localhost:8000", timeout=5)
        if response.status_code == 200 and "StudyWise" in response.text:
            print("✅ Website loads correctly")
            print("✅ You should be able to access http://localhost:8000")
            return True
        else:
            print(f"❌ Website issue - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Website error: {e}")
        return False

def main():
    print("🔍 DEBUG: Test 1.3 Login Issue")
    print("=" * 50)
    print("Testing the exact credentials from TEST_PLAN.md:")
    print("- Email: test@example.com")
    print("- Username: testuser123") 
    print("- Password: mypassword123")
    print("- Full Name: Test User")
    print("-" * 50)
    
    # Test website accessibility
    if not test_website_accessibility():
        print("❌ Cannot proceed - website not accessible")
        return
    
    # Test registration first
    registration_success = test_registration()
    
    if not registration_success:
        print("⚠️ Registration failed, but login might still work if user exists")
    
    # Test both login methods
    email_login = test_login_with_email()
    username_login = test_login_with_username()
    
    print("\n" + "=" * 50)
    print("🎯 DEBUG RESULTS SUMMARY")
    print("=" * 50)
    print(f"Registration:      {'✅ PASS' if registration_success else '❌ FAIL'}")
    print(f"Login with Email:  {'✅ PASS' if email_login else '❌ FAIL'}")
    print(f"Login with Username: {'✅ PASS' if username_login else '❌ FAIL'}")
    
    print(f"\n💡 RECOMMENDATIONS:")
    if email_login:
        print("✅ Use EMAIL (test@example.com) for login on the website")
    elif username_login:
        print("✅ Use USERNAME (testuser123) for login on the website")
    else:
        print("🔧 Neither login method works - check authentication system")
        print("🔧 Try these steps:")
        print("   1. Clear browser cache")
        print("   2. Check browser console for JavaScript errors (F12)")
        print("   3. Try different test credentials")
    
    print(f"\n🌐 To test manually:")
    print(f"   1. Go to http://localhost:8000")
    print(f"   2. Click Register, fill form, submit")
    print(f"   3. Click Login and try:")
    if email_login:
        print(f"      - Email: test@example.com")
    else:
        print(f"      - Username: testuser123") 
    print(f"      - Password: mypassword123")

if __name__ == "__main__":
    main()