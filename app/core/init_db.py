"""
Database initialization and setup utilities
"""
from app.core.database import create_tables, engine
from app.models.database import Base, User
from app.core.auth import get_password_hash
from sqlalchemy.orm import sessionmaker

def init_database():
    """Initialize the database with tables"""
    print("Creating database tables...")
    create_tables()
    print("Database tables created successfully!")

def create_test_user():
    """Create a test user for development"""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check if test user already exists
        existing_user = db.query(User).filter(User.email == "test@studywiseai.com").first()
        if existing_user:
            print("Test user already exists!")
            return
        
        # Create test user
        test_user = User(
            email="test@studywiseai.com",
            username="testuser",
            hashed_password=get_password_hash("testpassword123"),
            full_name="Test User",
            learning_style="visual",
            study_goals="Learn programming and AI fundamentals",
            is_active=True,
            is_verified=True
        )
        
        db.add(test_user)
        db.commit()
        print("Test user created successfully!")
        print("Email: test@studywiseai.com")
        print("Password: testpassword123")
        
    except Exception as e:
        print(f"Error creating test user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
    create_test_user()