#!/usr/bin/env python3
"""
Test script for Career Counseling feature
"""
import asyncio
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.services.ai_service import ai_service

async def test_career_counseling():
    """Test the career counseling AI functionality"""

    print("🧪 Testing Career Counseling Feature")
    print("=" * 50)

    # Test data
    test_user = type('User', (), {
        'learning_style': 'visual',
        'study_goals': 'Become a software engineer',
        'email': 'test@example.com'
    })()

    target_profession = "Software Engineer"

    print(f"🎯 Target Profession: {target_profession}")
    print(f"👤 User Learning Style: {test_user.learning_style}")
    print(f"🎓 User Goals: {test_user.study_goals}")
    print()

    # Test 1: Start career counseling
    print("📋 Test 1: Starting Career Counseling Session")
    print("-" * 40)

    try:
        result = await ai_service.start_career_counseling(test_user, target_profession)

        if result["success"]:
            print("✅ Career counseling started successfully!")
            print("🤖 AI Questions:")
            print(result["response"])
            print()

            # Test 2: Generate action plan
            print("📋 Test 2: Generating Career Action Plan")
            print("-" * 40)

            user_responses = """
            I am currently in high school with basic programming knowledge.
            I enjoy problem-solving and creating things.
            I have experience with Python basics and some web development.
            I want to start my career in 4 years after college.
            I am committed and willing to work hard.
            """

            result2 = await ai_service.generate_career_action_plan(
                test_user,
                target_profession,
                user_responses
            )

            if result2["success"]:
                print("✅ Career action plan generated successfully!")
                print("📝 Action Plan:")
                print(result2["response"])
                print()
                print("🎉 All tests passed! Career counseling feature is working.")
            else:
                print("❌ Failed to generate action plan:", result2.get("error", "Unknown error"))

        else:
            print("❌ Failed to start career counseling:", result.get("error", "Unknown error"))

    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_career_counseling())