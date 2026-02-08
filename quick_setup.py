"""
Quick setup script to create a test user and test the AI assistant
"""
import asyncio
import httpx
import json

async def setup_test_user():
    """Create a test user and test the AI assistant"""
    print("🚀 StudyWiseAI Quick Setup & Demo")
    print("=" * 40)
    
    base_url = "http://127.0.0.1:8000/api"
    
    # Test user data
    test_user = {
        "email": "student@example.com",
        "username": "student123",
        "password": "study2026",
        "full_name": "Test Student"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            print("\n1️⃣ Creating test user account...")
            
            # Register user
            register_response = await client.post(
                f"{base_url}/auth/register",
                json=test_user
            )
            
            if register_response.status_code == 200:
                print("✅ Test user created successfully!")
                print(f"📧 Email: {test_user['email']}")
                print(f"🔑 Password: {test_user['password']}")
            else:
                print("ℹ️ User might already exist, trying login...")
            
            print("\n2️⃣ Logging in...")
            
            # Login to get token
            login_data = {
                "username": test_user["email"],  # FastAPI uses username field for email
                "password": test_user["password"]
            }
            
            login_response = await client.post(
                f"{base_url}/auth/login",
                data=login_data
            )
            
            if login_response.status_code == 200:
                login_result = login_response.json()
                token = login_result["access_token"]
                print("✅ Login successful!")
                print(f"👤 Welcome, {login_result['user']['full_name']}!")
                
                # Test AI chat
                print("\n3️⃣ Testing AI Assistant...")
                
                headers = {"Authorization": f"Bearer {token}"}
                chat_request = {
                    "message": "Hi! Can you help me create a study plan for learning Python programming?",
                    "context": None
                }
                
                chat_response = await client.post(
                    f"{base_url}/ai/chat",
                    json=chat_request,
                    headers=headers,
                    timeout=30.0
                )
                
                if chat_response.status_code == 200:
                    chat_result = chat_response.json()
                    print("✅ AI Assistant is working!")
                    print(f"🤖 AI Response: {chat_result['response'][:200]}...")
                    print("\n🎉 Setup complete! Your free AI tutor is ready!")
                else:
                    print(f"⚠️ AI test failed: {chat_response.status_code}")
                    print("But the user account works - you can test AI via the web interface")
                    
            else:
                error_detail = login_response.json().get("detail", "Unknown error")
                print(f"❌ Login failed: {error_detail}")
                
        except httpx.ConnectError:
            print("❌ Cannot connect to StudyWiseAI server")
            print("Make sure the server is running: uvicorn app.main:app --reload")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 40)
    print("🌐 Access your StudyWiseAI app at: http://127.0.0.1:8000")
    print("📖 API docs at: http://127.0.0.1:8000/docs")
    print("💰 Cost so far: $0.00 (FREE!)")

if __name__ == "__main__":
    asyncio.run(setup_test_user())