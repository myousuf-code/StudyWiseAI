#!/usr/bin/env python3
"""
Direct database test to isolate authentication issues
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, create_tables
from app.models.database import User
from app.core.auth import get_password_hash, verify_password

def test_direct_auth():
    """Test authentication functions directly"""
    print("Testing direct authentication functions...")
    
    # Test password hashing
    try:
        test_password = "test123456"
        print(f"Testing password hash for: {test_password}")
        
        hashed = get_password_hash(test_password)
        print(f"✅ Password hashed successfully: {hashed[:20]}...")
        
        # Test password verification
        is_valid = verify_password(test_password, hashed)
        print(f"✅ Password verification: {is_valid}")
        
        if not is_valid:
            print("❌ Password verification failed!")
            return False
            
    except Exception as e:
        print(f"❌ Password hashing failed: {e}")
        return False
    
    # Test database connection
    try:
        print("\nTesting database connection...")
        db = SessionLocal()
        
        # Check if user table exists and can be queried
        user_count = db.query(User).count()
        print(f"✅ Database connected. Current users: {user_count}")
        
        # Try to create a test user directly in database
        test_user = User(
            email="dbtest@example.com",
            username="dbtest",
            hashed_password=hashed,
            full_name="DB Test User"
        )
        
        # Check if user already exists
        existing = db.query(User).filter(User.email == "dbtest@example.com").first()
        if existing:
            print("Deleting existing test user...")
            db.delete(existing)
            db.commit()
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print(f"✅ User created successfully with ID: {test_user.id}")
        
        # Clean up
        db.delete(test_user)
        db.commit()
        print("✅ Test user cleaned up")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
def main():
    print("StudyWiseAI Direct Authentication Test")
    print("=" * 40)
    
    # Initialize database
    try:
        create_tables()
        print("✅ Database initialized")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return
    
    # Run direct auth test
    success = test_direct_auth()
    
    if success:
        print("\n🎉 All direct authentication tests passed!")
    else:
        print("\n💥 Some tests failed!")

if __name__ == "__main__":
    main()