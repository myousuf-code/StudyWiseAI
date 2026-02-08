#!/usr/bin/env python3
"""
Comprehensive AI Features Test
Tests all AI tools and features integrated in StudyWiseAI
"""
import requests
import json
import random
import time

class StudyWiseAITester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.auth_token = None
        self.user_data = None
        
    def test_registration_and_login(self):
        """Test user registration and login to get auth token"""
        print("🔐 Testing Authentication...")
        
        # Generate unique user data
        user_id = random.randint(1000, 9999)
        test_user = {
            "email": f"aitest{user_id}@example.com",
            "username": f"aitest{user_id}",
            "password": "testpass123",
            "full_name": "AI Test User"
        }
        
        # Register user
        try:
            response = requests.post(f"{self.api_url}/auth/register", json=test_user)
            if response.status_code == 200:
                print("✅ User registration successful")
            else:
                print(f"❌ Registration failed: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Registration error: {e}")
            return False
        
        # Login to get auth token
        try:
            login_data = {
                "username": test_user["email"],
                "password": test_user["password"]
            }
            response = requests.post(f"{self.api_url}/auth/login", data=login_data)
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data["access_token"]
                self.user_data = data["user"]
                print(f"✅ Login successful, token obtained")
                return True
            else:
                print(f"❌ Login failed: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    def get_headers(self):
        """Get authorization headers"""
        return {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }
    
    def test_ai_chat(self):
        """Test AI chat assistant functionality"""
        print("\n💬 Testing AI Chat Assistant...")
        
        test_questions = [
            "How can I improve my study habits?",
            "What's the best way to memorize vocabulary?",
            "Can you help me create a study schedule for math?",
            "Give me tips for staying focused during study sessions"
        ]
        
        success_count = 0
        for i, question in enumerate(test_questions, 1):
            try:
                response = requests.post(
                    f"{self.api_url}/ai/chat",
                    headers=self.get_headers(),
                    json={"message": question, "context": None}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Chat {i}/4: Question answered successfully")
                    print(f"   Q: {question}")
                    print(f"   A: {data['response'][:100]}...")
                    success_count += 1
                else:
                    print(f"❌ Chat {i}/4 failed: {response.text}")
                
                # Small delay to avoid overwhelming the AI model
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ Chat {i}/4 error: {e}")
        
        print(f"📊 AI Chat Success Rate: {success_count}/{len(test_questions)} ({success_count/len(test_questions)*100:.0f}%)")
        return success_count > 0
    
    def test_study_plan_generation(self):
        """Test AI study plan generation"""
        print("\n📚 Testing Study Plan Generation...")
        
        test_plans = [
            {"subject": "Python Programming", "duration_weeks": 4, "difficulty_level": "beginner"},
            {"subject": "Calculus", "duration_weeks": 6, "difficulty_level": "intermediate"},
            {"subject": "Spanish", "duration_weeks": 8, "difficulty_level": "beginner"}
        ]
        
        success_count = 0
        for i, plan_data in enumerate(test_plans, 1):
            try:
                response = requests.post(
                    f"{self.api_url}/ai/generate-study-plan",
                    headers=self.get_headers(),
                    json=plan_data
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Study Plan {i}/3: Generated successfully for {plan_data['subject']}")
                    # Note: The API endpoint might return different structure
                    print(f"   Subject: {data.get('subject', plan_data['subject'])}")
                    print(f"   Duration: {data.get('duration_weeks', plan_data['duration_weeks'])} weeks")
                    success_count += 1
                else:
                    print(f"❌ Study Plan {i}/3 failed: {response.text}")
                
                time.sleep(2)  # Longer delay for study plan generation
                
            except Exception as e:
                print(f"❌ Study Plan {i}/3 error: {e}")
        
        print(f"📊 Study Plan Generation Success Rate: {success_count}/{len(test_plans)} ({success_count/len(test_plans)*100:.0f}%)")
        return success_count > 0
    
    def test_quiz_generation(self):
        """Test AI quiz question generation"""
        print("\n🧠 Testing Quiz Generation...")
        
        quiz_requests = [
            {"topic": "Python basics", "difficulty": "beginner", "question_count": 3},
            {"topic": "World History", "difficulty": "intermediate", "question_count": 2},
            {"topic": "Biology cells", "difficulty": "advanced", "question_count": 2}
        ]
        
        success_count = 0
        for i, quiz_data in enumerate(quiz_requests, 1):
            try:
                response = requests.post(
                    f"{self.api_url}/ai/generate-quiz",
                    headers=self.get_headers(),
                    json=quiz_data
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Quiz {i}/3: Generated successfully for {quiz_data['topic']}")
                    print(f"   Topic: {data.get('topic', quiz_data['topic'])}")
                    print(f"   Questions: {data.get('question_count', quiz_data['question_count'])}")
                    success_count += 1
                else:
                    print(f"❌ Quiz {i}/3 failed: {response.text}")
                
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ Quiz {i}/3 error: {e}")
        
        print(f"📊 Quiz Generation Success Rate: {success_count}/{len(quiz_requests)} ({success_count/len(quiz_requests)*100:.0f}%)")
        return success_count > 0
    
    def test_progress_insights(self):
        """Test AI progress analysis"""
        print("\n📈 Testing Progress Insights...")
        
        # First, create some dummy progress data
        try:
            # Create a dummy progress record
            progress_data = {
                "subject": "Python Programming",
                "topic": "Variables and Data Types",
                "time_spent": 45,
                "accuracy_score": 85,
                "difficulty_level": "beginner"
            }
            
            # Note: This endpoint might not exist yet, so we'll test the insights endpoint directly
            response = requests.get(
                f"{self.api_url}/ai/progress-insights",
                headers=self.get_headers()
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Progress insights generated successfully")
                print(f"   Insights: {str(data.get('insights', 'No insights available'))[:100]}...")
                return True
            else:
                print(f"❌ Progress insights failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Progress insights error: {e}")
            return False
    
    def test_chat_history(self):
        """Test chat history retrieval"""
        print("\n📜 Testing Chat History...")
        
        try:
            response = requests.get(
                f"{self.api_url}/ai/chat-history",
                headers=self.get_headers()
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Chat history retrieved successfully")
                print(f"   Messages: {len(data)} chat messages")
                return True
            else:
                print(f"❌ Chat history failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Chat history error: {e}")
            return False
    
    def run_comprehensive_test(self):
        """Run all AI feature tests"""
        print("🤖 StudyWiseAI - Comprehensive AI Features Test")
        print("=" * 50)
        
        # Test authentication first
        if not self.test_registration_and_login():
            print("❌ Authentication failed - cannot proceed with AI tests")
            return
        
        # Test AI features
        test_results = {
            "AI Chat": self.test_ai_chat(),
            "Study Plan Generation": self.test_study_plan_generation(),
            "Quiz Generation": self.test_quiz_generation(), 
            "Progress Insights": self.test_progress_insights(),
            "Chat History": self.test_chat_history()
        }
        
        # Summary
        print("\n" + "=" * 50)
        print("🎯 AI Features Test Summary")
        print("=" * 50)
        
        passed = sum(test_results.values())
        total = len(test_results)
        
        for feature, result in test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{feature:<25} {status}")
        
        print(f"\n📊 Overall Result: {passed}/{total} features working ({passed/total*100:.0f}%)")
        
        if passed == total:
            print("🎉 All AI features are working perfectly!")
        elif passed > total // 2:
            print("⚠️ Most AI features are working - some need attention")
        else:
            print("🔧 Several AI features need fixing")

def main():
    # Check if server is running
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code != 200:
            print("❌ StudyWiseAI server is not responding. Please start the server first.")
            print("Run: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000")
            return
    except:
        print("❌ Cannot connect to StudyWiseAI server at http://localhost:8000")
        print("Please make sure the server is running.")
        return
    
    # Run comprehensive test
    tester = StudyWiseAITester()
    tester.run_comprehensive_test()

if __name__ == "__main__":
    main()