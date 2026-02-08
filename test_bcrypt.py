#!/usr/bin/env python3
"""
Simple bcrypt test to diagnose the issue
"""
import bcrypt

def test_bcrypt_directly():
    """Test bcrypt directly without passlib"""
    print("Testing bcrypt directly...")
    
    try:
        password = "test123456"
        print(f"Password: {password} (length: {len(password)} chars, {len(password.encode('utf-8'))} bytes)")
        
        # Hash the password
        password_bytes = password.encode('utf-8')
        hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        print(f"✅ Password hashed successfully: {hashed}")
        
        # Verify the password
        is_valid = bcrypt.checkpw(password_bytes, hashed)
        print(f"✅ Password verification: {is_valid}")
        
        return True
        
    except Exception as e:
        print(f"❌ bcrypt test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_passlib_simple():
    """Test passlib with a very simple configuration"""
    print("\nTesting passlib with simple configuration...")
    
    try:
        from passlib.hash import bcrypt as passlib_bcrypt
        
        password = "test123456"
        print(f"Password: {password}")
        
        # Hash the password
        hashed = passlib_bcrypt.hash(password)
        print(f"✅ Password hashed successfully: {hashed}")
        
        # Verify the password
        is_valid = passlib_bcrypt.verify(password, hashed)
        print(f"✅ Password verification: {is_valid}")
        
        return True
        
    except Exception as e:
        print(f"❌ passlib simple test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Bcrypt Diagnosis Test")
    print("=" * 30)
    
    success1 = test_bcrypt_directly()
    success2 = test_passlib_simple()
    
    if success1 and success2:
        print("\n🎉 All bcrypt tests passed!")
    else:
        print("\n💥 Some bcrypt tests failed!")