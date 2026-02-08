#!/usr/bin/env python3
"""
StudyWiseAI - Quick AI Response Time Test
Tests AI response speed to diagnose "stuck on thinking" issues
"""

import requests
import time
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

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

def quick_login():
    """Quick login with fresh credentials"""
    try:
        # Use existing user or create fresh one
        login_data = {
            "username": "fresh1234@example.com",
            "password": "freshpass123"
        }
        
        response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data, timeout=10)
        
        if response.status_code == 200:
            token = response.json().get("access_token")
            print_status("Logged in successfully", "SUCCESS")
            return token
        else:
            print_status(f"Login failed: {response.status_code}", "FAIL")
            return None
            
    except Exception as e:
        print_status(f"Login error: {e}", "FAIL")
        return None

def test_ai_response_time(token, question, timeout=30):
    """Test single AI response time"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        data = {"message": question}
        
        print_status(f"Asking AI: '{question[:50]}...'", "INFO")
        start_time = time.time()
        
        response = requests.post(
            f"{BASE_URL}/api/ai/chat", 
            json=data, 
            headers=headers, 
            timeout=timeout
        )
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        if response.status_code == 200:
            result = response.json()
            response_text = result.get("response", "")[:100]
            print_status(f"✅ Response in {elapsed:.1f}s: {response_text}...", "SUCCESS")
            return True, elapsed
        else:
            print_status(f"❌ AI request failed: {response.status_code}", "FAIL")
            return False, elapsed
            
    except requests.exceptions.Timeout:
        print_status(f"⚠️ AI request timed out after {timeout}s", "WARN")
        return False, timeout
    except Exception as e:
        print_status(f"❌ AI request error: {e}", "FAIL")
        return False, 0

def main():
    """Run quick AI speed tests"""
    print("🚀 StudyWiseAI - Quick AI Response Time Test")
    print("=" * 55)
    
    # Check server
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print_status("Server is running", "SUCCESS")
        else:
            print_status("Server check failed", "FAIL")
            return
    except:
        print_status("Cannot connect to server", "FAIL")
        return
    
    # Login
    token = quick_login()
    if not token:
        print_status("Cannot proceed without authentication", "FAIL")
        return
    
    # Test different AI requests with increasing complexity
    test_questions = [
        ("Hi", "Simple greeting"),
        ("What is 2+2?", "Basic math"),
        ("How to study better?", "Study advice"),
        ("Create a study plan for math", "Complex request")
    ]
    
    results = []
    
    for question, description in test_questions:
        print(f"\n📝 Testing: {description}")
        success, elapsed = test_ai_response_time(token, question, timeout=45)
        results.append((description, success, elapsed))
        
        if not success and elapsed >= 45:
            print_status("Stopping tests due to timeout", "WARN")
            break
    
    # Results summary
    print("\n" + "=" * 55)
    print("📊 AI RESPONSE TIME SUMMARY")
    print("=" * 55)
    
    total_tests = len(results)
    successful_tests = sum(1 for _, success, _ in results if success)
    
    for description, success, elapsed in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{description:<20} {elapsed:>6.1f}s  {status}")
    
    avg_time = sum(elapsed for _, success, elapsed in results if success) / max(successful_tests, 1)
    
    print("-" * 55)
    print(f"Tests Passed: {successful_tests}/{total_tests}")
    print(f"Average Response Time: {avg_time:.1f}s")
    
    # Provide recommendations
    print("\n🎯 RECOMMENDATIONS:")
    if avg_time > 20:
        print("⚠️ Response times are slow (>20s)")
        print("   • This explains the 'stuck on thinking' issue")
        print("   • Consider shorter questions for testing")
        print("   • AI model runs on CPU (normal but slower)")
    elif avg_time > 10:
        print("✅ Response times are acceptable (10-20s)")
        print("   • Normal for local AI on CPU")
        print("   • Users should expect 10-15s wait times")
    else:
        print("🚀 Response times are excellent (<10s)")
        print("   • AI is performing well!")
    
    print("\n💡 FRONTEND IMPROVEMENTS:")
    print("   • Add progress indicators during AI thinking")
    print("   • Show 'AI is thinking...' animation")
    print("   • Set user expectations (10-15s typical)")
    print("   • Add cancel button for long requests")

if __name__ == "__main__":
    main()