#!/usr/bin/env python3
"""
Test script for career counseling and career action plan generation
"""
import requests
import json
import time

def test_career_flow():
    base_url = "http://localhost:8000"
    
    print("=" * 60)
    print("Testing Career Counseling Full Flow")
    print("=" * 60)
    
    # Register and login
    print("\n1. Creating test user...")
    
    try:
        reg_response = requests.post(
            f"{base_url}/api/auth/register",
            json={
                "email": "testcareerflow@example.com",
                "username": "testcareerflow",
                "password": "testpass123",
                "full_name": "Test Career Flow User"
            }
        )
        print(f"   Registration: {reg_response.status_code}")
    except Exception as e:
        print(f"   Registration might have failed (user exists?): {e}")
    
    # Login
    print("\n2. Logging in...")
    try:
        login_response = requests.post(
            f"{base_url}/api/auth/login",
            data={
                "username": "testcareerflow@example.com",
                "password": "testpass123"
            }
        )
        print(f"   Login status: {login_response.status_code}")
        
        if login_response.status_code != 200:
            print(f"   Error: {login_response.text}")
            return
        
        token_data = login_response.json()
        token = token_data["access_token"]
        print("   ✅ Got authentication token!")
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test 1: Start career counseling
        print("\n3. Starting career counseling...")
        start_time = time.time()
        
        response = requests.post(
            f"{base_url}/api/ai/career-counseling/start",
            headers=headers,
            json={"target_profession": "Software Engineer"},
            timeout=60
        )
        
        elapsed = time.time() - start_time
        print(f"   Time: {elapsed:.2f}s | Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   ❌ Error: {response.text}")
            return
        
        counseling_data = response.json()
        session_id = counseling_data["session_id"]
        questions = counseling_data["initial_questions"]
        
        print(f"   ✅ Session created: ID {session_id}")
        print(f"   Questions: {questions[:100]}...")
        
        # Test 2: Generate career action plan
        print("\n4. Generating career action plan...")
        start_time = time.time()
        
        plan_response = requests.post(
            f"{base_url}/api/ai/career-counseling/generate-plan",
            headers=headers,
            json={
                "target_profession": "Software Engineer",
                "user_responses": """
                I'm currently a high school senior with strong math and computer science grades.
                I've done some programming in Python and Java. I'm very interested in building
                applications and solving real-world problems. I plan to study computer science
                at university and eventually work at a tech company. I can dedicate 3-4 hours
                daily to learning outside of school.
                """
            },
            timeout=90
        )
        
        elapsed = time.time() - start_time
        print(f"   Time: {elapsed:.2f}s | Status: {plan_response.status_code}")
        
        if plan_response.status_code != 200:
            print(f"   ❌ Error: {plan_response.text}")
            return
        
        plan_data = plan_response.json()
        action_plan = plan_data["action_plan"]
        
        print(f"   ✅ Action plan generated!")
        print(f"   Preview: {action_plan[:150]}...")
        
        # Test 3: Convert to study plan
        print("\n5. Converting career plan to study plan...")
        start_time = time.time()
        
        convert_response = requests.post(
            f"{base_url}/api/ai/career-counseling/convert-to-study-plan",
            headers=headers,
            json={
                "session_id": session_id,
                "plan_title": "Software Engineer Career Path"
            },
            timeout=60
        )
        
        elapsed = time.time() - start_time
        print(f"   Time: {elapsed:.2f}s | Status: {convert_response.status_code}")
        
        if convert_response.status_code != 200:
            print(f"   ❌ Error: {convert_response.text}")
            return
        
        convert_data = convert_response.json()
        study_plan_id = convert_data["study_plan_id"]
        tasks_created = convert_data["tasks_created"]
        
        print(f"   ✅ Study plan created!")
        print(f"   Study Plan ID: {study_plan_id}")
        print(f"   Tasks Created: {tasks_created}")
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print(f"\nCareer Counseling Flow Summary:")
        print(f"  - Session ID: {session_id}")
        print(f"  - Study Plan ID: {study_plan_id}")
        print(f"  - Tasks Generated: {tasks_created}")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_career_flow()
