#!/usr/bin/env python3
"""
Direct AI Features Test using FastAPI TestClient
Tests AI features directly without HTTP requests
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

class DirectAITester:
    def __init__(self):
        self.auth_token = None
        self.user_data = None
        
        # Initialize database
        create_tables()
    
    def register_and_login(self):
        """Register a test user and get auth token"""
        print("🔐 Setting up test user...")
        
        # Generate unique user
        user_id = random.randint(1000, 9999)
        test_user = {
            "email": f"aitest{user_id}@example.com",
            "username": f"aitest{user_id}",
            "password": "testpass123",
            "full_name": "AI Test User"
        }
        
        # Register
        response = client.post("/api/auth/register", json=test_user)
        if response.status_code != 200:
            print(f"❌ Registration failed: {response.text}")
            return False
        
        # Login
        login_data = {
            "username": test_user["email"],
            "password": test_user["password"]
        }
        response = client.post("/api/auth/login", data=login_data)
        if response.status_code != 200:
            print(f"❌ Login failed: {response.text}")
            return False
        
        data = response.json()
        self.auth_token = data["access_token"]
        self.user_data = data["user"]
        print("✅ Test user authenticated successfully")
        return True
    
    def get_headers(self):
        """Get authorization headers"""
        return {"Authorization": f"Bearer {self.auth_token}"}
    
    def test_ai_chat(self):
        """Test AI chat functionality"""
        print("\n💬 Testing AI Chat Assistant...")
        
        test_messages = [
            "Hello! Can you help me study?",
            "What's the best way to learn Python programming?",
            "How can I stay motivated while studying?",
            "Can you explain what machine learning is?"
        ]
        
        success_count = 0
        for i, message in enumerate(test_messages, 1):
            try:
                response = client.post(
                    "/api/ai/chat",
                    headers=self.get_headers(),
                    json={"message": message, "context": None}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Chat {i}/{len(test_messages)}: Response received")
                    print(f"   Q: {message}")
                    print(f"   A: {data['response'][:80]}...")
                    success_count += 1
                else:
                    print(f"❌ Chat {i}/{len(test_messages)} failed: {response.status_code}")
                    print(f"   Error: {response.text}")
                    
            except Exception as e:
                print(f"❌ Chat {i}/{len(test_messages)} error: {e}")
        
        return success_count, len(test_messages)
    
    def test_study_plan_generation(self):
        """Test study plan generation"""
        print("\n📚 Testing Study Plan Generation...")
        
        test_plans = [
            {"subject": "Python Programming", "duration_weeks": 4, "difficulty_level": "beginner"},
            {"subject": "Mathematics", "duration_weeks": 6, "difficulty_level": "intermediate"}
        ]
        
        success_count = 0
        for i, plan in enumerate(test_plans, 1):
            try:
                response = client.post(
                    "/api/ai/generate-study-plan",
                    headers=self.get_headers(),
                    json=plan
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Study Plan {i}/{len(test_plans)}: Generated for {plan['subject']}")
                    success_count += 1
                else:
                    print(f"❌ Study Plan {i}/{len(test_plans)} failed: {response.status_code}")
                    print(f"   Error: {response.text}")
                    
            except Exception as e:
                print(f"❌ Study Plan {i}/{len(test_plans)} error: {e}")
        
        return success_count, len(test_plans)
    
    def test_quiz_generation(self):
        """Test quiz generation"""
        print("\n🧠 Testing Quiz Generation...")
        
        quiz_tests = [
            {"topic": "Python basics", "difficulty": "beginner", "question_count": 3},
            {"topic": "World History", "difficulty": "intermediate", "question_count": 2}
        ]
        
        success_count = 0
        for i, quiz in enumerate(quiz_tests, 1):
            try:
                response = client.post(
                    "/api/ai/generate-quiz",
                    headers=self.get_headers(),
                    json=quiz
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Quiz {i}/{len(quiz_tests)}: Generated for {quiz['topic']}")
                    success_count += 1
                else:
                    print(f"❌ Quiz {i}/{len(quiz_tests)} failed: {response.status_code}")
                    print(f"   Error: {response.text}")
                    
            except Exception as e:
                print(f"❌ Quiz {i}/{len(quiz_tests)} error: {e}")
        
        return success_count, len(quiz_tests)
    
    def test_progress_insights(self):
        """Test progress insights"""
        print("\n📈 Testing Progress Insights...")
        
        try:
            response = client.get(
                "/api/ai/progress-insights",
                headers=self.get_headers()
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Progress Insights: Generated successfully")
                insights = data.get("insights", "No insights available")
                print(f"   Insights: {insights[:80]}...")
                return 1, 1
            else:
                print(f"❌ Progress Insights failed: {response.status_code}")
                print(f"   Error: {response.text}")
                return 0, 1
                
        except Exception as e:
            print(f"❌ Progress Insights error: {e}")
            return 0, 1
    
    def test_chat_history(self):
        """Test chat history"""
        print("\n📜 Testing Chat History...")
        
        try:
            response = client.get(
                "/api/ai/chat-history",
                headers=self.get_headers()
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Chat History: Retrieved {len(data)} messages")
                return 1, 1
            else:
                print(f"❌ Chat History failed: {response.status_code}")
                return 0, 1
                
        except Exception as e:
            print(f"❌ Chat History error: {e}")
            return 0, 1
    
    def test_frontend_availability(self):
        """Test if frontend is available"""
        print("\n🌐 Testing Frontend Availability...")
        
        try:
            response = client.get("/")
            if response.status_code == 200:
                print("✅ Frontend: Home page loads successfully")
                return 1, 1
            else:
                print(f"❌ Frontend failed: {response.status_code}")
                return 0, 1
                
        except Exception as e:
            print(f"❌ Frontend error: {e}")
            return 0, 1
    
    def run_comprehensive_test(self):
        """Run all AI feature tests"""
        print("🤖 StudyWiseAI - Direct AI Features Test")
        print("=" * 50)
        
        # Setup authentication
        if not self.register_and_login():
            print("❌ Authentication setup failed")
            return
        
        # Run tests
        test_results = {}
        
        # Test individual features
        chat_pass, chat_total = self.test_ai_chat()
        test_results["AI Chat Assistant"] = (chat_pass, chat_total)
        
        plan_pass, plan_total = self.test_study_plan_generation()
        test_results["Study Plan Generation"] = (plan_pass, plan_total)
        
        quiz_pass, quiz_total = self.test_quiz_generation()
        test_results["Quiz Generation"] = (quiz_pass, quiz_total)
        
        insights_pass, insights_total = self.test_progress_insights()
        test_results["Progress Insights"] = (insights_pass, insights_total)
        
        history_pass, history_total = self.test_chat_history()
        test_results["Chat History"] = (history_pass, history_total)
        
        frontend_pass, frontend_total = self.test_frontend_availability()
        test_results["Frontend Website"] = (frontend_pass, frontend_total)
        
        # Summary
        print("\n" + "=" * 60)
        print("🎯 AI FEATURES INTEGRATION SUMMARY")
        print("=" * 60)
        
        total_passed = 0
        total_tests = 0
        
        for feature, (passed, total) in test_results.items():
            percentage = (passed/total*100) if total > 0 else 0
            status = "✅ WORKING" if passed == total else f"⚠️ PARTIAL ({passed}/{total})" if passed > 0 else "❌ FAILED"
            print(f"{feature:<25} {status:>15} ({percentage:3.0f}%)")
            total_passed += passed
            total_tests += total
        
        overall_percentage = (total_passed/total_tests*100) if total_tests > 0 else 0
        
        print("-" * 60)
        print(f"{'OVERALL INTEGRATION':<25} {total_passed:>3}/{total_tests:<3} tests ({overall_percentage:3.0f}%)")
        
        print("\n📋 FEATURE STATUS REPORT:")
        print("-" * 30)
        
        # Detailed analysis
        working_features = []
        partial_features = []
        broken_features = []
        
        for feature, (passed, total) in test_results.items():
            if passed == total:
                working_features.append(feature)
            elif passed > 0:
                partial_features.append(f"{feature} ({passed}/{total})")
            else:
                broken_features.append(feature)
        
        if working_features:
            print(f"✅ FULLY WORKING: {', '.join(working_features)}")
        
        if partial_features:
            print(f"⚠️ PARTIALLY WORKING: {', '.join(partial_features)}")
        
        if broken_features:
            print(f"❌ NOT WORKING: {', '.join(broken_features)}")
        
        # Final verdict
        print("\n🎯 INTEGRATION VERDICT:")
        if overall_percentage >= 90:
            print("🎉 EXCELLENT! Almost all AI features are fully integrated and working!")
        elif overall_percentage >= 70:
            print("✅ GOOD! Most AI features are integrated and ready to use.")
        elif overall_percentage >= 50:
            print("⚠️ PARTIAL! Several AI features are working but some need attention.")
        else:
            print("🔧 NEEDS WORK! Many AI features require fixes before deployment.")

def main():
    print("Starting Direct AI Features Integration Test...\n")
    
    tester = DirectAITester()
    tester.run_comprehensive_test()

if __name__ == "__main__":
    main()