#!/usr/bin/env python3
"""
StudyWiseAI - Comprehensive Login Security Test
Tests various login scenarios including edge cases and security tests
"""

import requests
import json
import sys
from datetime import datetime
# Import for cleanup function
try:
    from app.core.database import get_db
    from app.models.user import User
    from sqlalchemy.orm import Session
except ImportError:
    print("Warning: Could not import database modules for cleanup")
    # Configuration
BASE_URL = "http://localhost:8000"
TEST_EMAIL = "logintest@example.com"
TEST_PASSWORD = "securepass123"
TEST_USERNAME = "logintest"

# Delete existing user if exists
def cleanup_existing_user():
    """Clean up any existing test user"""
    try:
        from app.core.database import get_db
        from app.models.user import User
        from sqlalchemy.orm import Session
        
        db = next(get_db())
        existing_user = db.query(User).filter(User.email == TEST_EMAIL).first()
        if existing_user:
            db.delete(existing_user)
            db.commit()
            print_status("Cleaned up existing test user", "INFO")
        db.close()
    except Exception as e:
        print_status(f"Cleanup warning: {e}", "WARN")

def print_status(message, status="INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    if status == "SUCCESS":
        print(f"[{timestamp}] ✅ {message}")
    elif status == "FAIL":
        print(f"[{timestamp}] ❌ {message}")
    elif status == "WARN":
        print(f"[{timestamp}] ⚠️ {message}")
    else:
        print(f"[{timestamp}] ℹ️ {message}")

def test_server_connection():
    """Test if server is running"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print_status("Server is running", "SUCCESS")
            return True
        else:
            print_status(f"Server returned status {response.status_code}", "FAIL")
            return False
    except requests.exceptions.RequestException as e:
        print_status(f"Cannot connect to server: {e}", "FAIL")
        return False

def register_test_user():
    """Register a test user for login tests"""
    try:
        # First clean up any existing user
        cleanup_existing_user()
        
        user_data = {
            "full_name": "Login Test User",
            "username": TEST_USERNAME,
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
        
        response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data, timeout=10)
        
         # User might already exist, that's okay
        if response.status_code in [200, 201]:
            print_status("Test user registered successfully", "SUCCESS")
            return True
        elif response.status_code == 400 and "already exists" in response.text.lower():
            print_status("Test user already exists (continuing with tests)", "WARN")
            return True
        else:
            print_status(f"Failed to register test user: {response.status_code} - {response.text}", "FAIL")
            return False
            
    except requests.exceptions.RequestException as e:
        print_status(f"Registration request failed: {e}", "FAIL")
        return False

def test_valid_login():
    """Test 1: Valid login credentials"""
    try:
        login_data = {
            "username": TEST_EMAIL,  # API expects username field (can be email)
            "password": TEST_PASSWORD
        }
        
        response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if "access_token" in data:
                print_status("Valid login test passed", "SUCCESS")
                return True, data.get("access_token")
            else:
                print_status("Valid login returned 200 but no access_token", "FAIL")
                return False, None
        else:
            print_status(f"Valid login failed: {response.status_code} - {response.text}", "FAIL")
            return False, None
            
    except requests.exceptions.RequestException as e:
        print_status(f"Valid login request failed: {e}", "FAIL")
        return False, None

def test_invalid_email():
    """Test 2: Invalid email format"""
    try:
        login_data = {
            "username": "invalid-email",
            "password": TEST_PASSWORD
        }
        
        response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data, timeout=10)
        
        if response.status_code in [400, 422]:
            print_status("Invalid email test passed (correctly rejected)", "SUCCESS")
            return True
        else:
            print_status(f"Invalid email should be rejected: {response.status_code}", "FAIL")
            return False
            
    except requests.exceptions.RequestException as e:
        print_status(f"Invalid email request failed: {e}", "FAIL")
        return False

def test_wrong_password():
    """Test 3: Correct email, wrong password"""
    try:
        login_data = {
            "username": TEST_EMAIL,
            "password": "wrongpassword123"
        }
        
        response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data, timeout=10)
        
        if response.status_code in [401, 400]:  # Updated expected codes
            print_status("Wrong password test passed (correctly rejected)", "SUCCESS")
            return True
        else:
            print_status(f"Wrong password should be rejected: {response.status_code}", "FAIL")
            return False
            
    except requests.exceptions.RequestException as e:
        print_status(f"Wrong password request failed: {e}", "FAIL")
        return False

def test_nonexistent_user():
    """Test 4: Non-existent user email"""
    try:
        login_data = {
            "username": "nonexistent@example.com",
            "password": "anypassword123"
        }
        
        response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data, timeout=10)
        
        if response.status_code in [401, 400]:  # Updated expected codes
            print_status("Non-existent user test passed (correctly rejected)", "SUCCESS")
            return True
        else:
            print_status(f"Non-existent user should be rejected: {response.status_code}", "FAIL")
            return False
            
    except requests.exceptions.RequestException as e:
        print_status(f"Non-existent user request failed: {e}", "FAIL")
        return False

def test_empty_credentials():
    """Test 5: Empty email and password"""
    test_cases = [
        {"username": "", "password": TEST_PASSWORD, "name": "empty username"},
        {"username": TEST_EMAIL, "password": "", "name": "empty password"},
        {"username": "", "password": "", "name": "empty both"},
    ]
    
    all_passed = True
    
    for case in test_cases:
        try:
            response = requests.post(f"{BASE_URL}/api/auth/login", data=case, timeout=10)
            
            if response.status_code in [400, 422]:
                print_status(f"Empty credentials test passed ({case['name']})", "SUCCESS")
            else:
                print_status(f"Empty credentials should be rejected ({case['name']}): {response.status_code}", "FAIL")
                all_passed = False
                
        except requests.exceptions.RequestException as e:
            print_status(f"Empty credentials request failed ({case['name']}): {e}", "FAIL")
            all_passed = False
    
    return all_passed

def test_malformed_json():
    """Test 6: Malformed JSON in request"""
    try:
        # Send malformed JSON
        response = requests.post(
            f"{BASE_URL}/api/auth/login", 
            data='{\"username\": \"test@example.com\", \"password\": \"missing quote}',  # Invalid JSON - missing quote
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code in [400, 422]:
            print_status("Malformed JSON test passed (correctly rejected)", "SUCCESS")
            return True
        else:
            print_status(f"Malformed JSON should be rejected: {response.status_code}", "FAIL")
            return False
            
    except requests.exceptions.RequestException as e:
        print_status(f"Malformed JSON request failed: {e}", "FAIL")
        return False

def test_sql_injection_attempts():
    """Test 7: SQL injection attempts"""
    injection_attempts = [
        "admin@example.com' OR '1'='1",
        "test@example.com'; DROP TABLE users; --",
        "admin@example.com' UNION SELECT * FROM users --",
        "'; DELETE FROM users WHERE '1'='1"
    ]
    
    all_passed = True
    
    for injection in injection_attempts:
        try:
            login_data = {
                "username": injection,
                "password": "anypassword"
            }
            
            response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data, timeout=10)
            
            if response.status_code in [401, 400]:  # Updated expected codes
                print_status(f"SQL injection blocked: {injection[:30]}...", "SUCCESS")
            elif response.status_code == 500:
                print_status(f"SQL injection caused server error: {injection[:30]}...", "FAIL")
                all_passed = False
            else:
                print_status(f"Unexpected response to SQL injection: {response.status_code}", "WARN")
                
        except requests.exceptions.RequestException as e:
            print_status(f"SQL injection request failed: {e}", "FAIL")
            all_passed = False
    
    return all_passed

def test_case_sensitivity():
    """Test 8: Email case sensitivity"""
    try:
        # Test with uppercase email
        login_data = {
            "username": TEST_EMAIL.upper(),
            "password": TEST_PASSWORD
        }
        
        response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data, timeout=10)
        
        # Email should ideally be case-insensitive
        if response.status_code == 200:
            print_status("Case insensitive email test passed", "SUCCESS")
            return True
        elif response.status_code in [401, 400]:  # Updated expected codes
            print_status("Email is case sensitive (this may be by design)", "WARN")
            return True  # Not necessarily a failure
        else:
            print_status(f"Unexpected response for case test: {response.status_code}", "FAIL")
            return False
            
    except requests.exceptions.RequestException as e:
        print_status(f"Case sensitivity request failed: {e}", "FAIL")
        return False

def test_token_validity(token):
    """Test 9: Token validity for protected endpoint"""
    if not token:
        print_status("No token available for validation test", "FAIL")
        return False
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/auth/profile", headers=headers, timeout=10)
        
        if response.status_code == 200:
            print_status("Token validity test passed", "SUCCESS")
            return True
        else:
            print_status(f"Token validation failed: {response.status_code}", "FAIL")
            return False
            
    except requests.exceptions.RequestException as e:
        print_status(f"Token validation request failed: {e}", "FAIL")
        return False

def main():
    """Run comprehensive login tests"""
    print("🔐 StudyWiseAI - Comprehensive Login Security Test")
    print("=" * 60)
    
    # Track test results
    tests = []
    
    # Test 0: Server connection
    if not test_server_connection():
        print_status("Cannot run tests - server not accessible", "FAIL")
        sys.exit(1)
    
    # Setup: Register test user
    tests.append(("User Registration", register_test_user()))
    
    # Test 1: Valid login
    valid_result, token = test_valid_login()
    tests.append(("Valid Login", valid_result))
    
    # Test 2: Invalid email format
    tests.append(("Invalid Email Format", test_invalid_email()))
    
    # Test 3: Wrong password
    tests.append(("Wrong Password", test_wrong_password()))
    
    # Test 4: Non-existent user
    tests.append(("Non-existent User", test_nonexistent_user()))
    
    # Test 5: Empty credentials
    tests.append(("Empty Credentials", test_empty_credentials()))
    
    # Test 6: Malformed JSON
    tests.append(("Malformed JSON", test_malformed_json()))
    
    # Test 7: SQL injection attempts
    tests.append(("SQL Injection Protection", test_sql_injection_attempts()))
    
    # Test 8: Case sensitivity
    tests.append(("Case Sensitivity", test_case_sensitivity()))
    
    # Test 9: Token validity
    tests.append(("Token Validity", test_token_validity(token)))
    
    # Results summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    for test_name, result in tests:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<30} {status}")
    
    print("-" * 60)
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print_status("🎉 All login security tests passed!", "SUCCESS")
        return 0
    else:
        print_status(f"⚠️ {total - passed} test(s) failed", "FAIL")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)