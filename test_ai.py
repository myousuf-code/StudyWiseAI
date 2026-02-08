"""
Test script to verify GPT4All local AI integration
"""
import asyncio
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.services.ai_service import ai_service

async def test_local_ai():
    """Test the local AI service"""
    print("🧪 Testing StudyWiseAI Local AI Integration")
    print("=" * 50)
    
    # Test 1: Simple question
    print("\n1️⃣ Testing basic AI chat...")
    response = await ai_service.get_study_help(
        user=None,  # We'll pass None for this test
        question="What are the best study techniques for learning programming?",
        context=None
    )
    
    if response["success"]:
        print("✅ AI Response received!")
        print(f"💬 Response: {response['response'][:200]}...")
        print("✅ Local AI is working perfectly!")
    else:
        print("❌ AI Response failed:")
        print(f"Error: {response['error']}")
        
    # Test 2: Study plan generation
    print("\n2️⃣ Testing study plan generation...")
    
    # Create a mock user object for testing
    class MockUser:
        def __init__(self):
            self.learning_style = "visual"
            self.study_goals = "Learn Python programming"
            
    mock_user = MockUser()
    
    plan_response = await ai_service.generate_study_plan(
        user=mock_user,
        subject="Python Programming",
        duration_weeks=4,
        difficulty_level="beginner",
        learning_style="visual"
    )
    
    if plan_response["success"]:
        print("✅ Study plan generated successfully!")
        print(f"📚 Plan: {plan_response['response'][:300]}...")
    else:
        print("❌ Study plan generation failed:")
        print(f"Error: {plan_response['error']}")
        
    print("\n🎉 Local AI testing complete!")
    print("💰 Cost: $0.00 (completely free!)")

if __name__ == "__main__":
    asyncio.run(test_local_ai())