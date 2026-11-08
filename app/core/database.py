"""
Database Connection and Session Management
"""
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.database import Base

# Create SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG  # Log SQL queries in debug mode
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables (for development - in production use Alembic)
def create_tables():
    """Create all tables in the database"""
    Base.metadata.create_all(bind=engine)
    _ensure_user_verification_columns()


def _ensure_user_verification_columns():
    """Add verification columns for existing installs without a migration tool."""
    inspector = inspect(engine)
    if "users" not in inspector.get_table_names():
        return

    existing_columns = {column["name"] for column in inspector.get_columns("users")}
    missing_columns = {
        "email_verification_token": "VARCHAR(255)",
        "email_verification_expires_at": "DATETIME",
        "email_verification_sent_at": "DATETIME",
    }

    with engine.begin() as connection:
        for column_name, column_type in missing_columns.items():
            if column_name not in existing_columns:
                connection.execute(text(f"ALTER TABLE users ADD COLUMN {column_name} {column_type}"))

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Redis connection (for caching and real-time features)
redis_client = None
try:
    import redis
    from app.core.config import settings
    redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
except ImportError:
    # Redis is optional for development
    print("Warning: Redis not available - some features may be limited")
except Exception as e:
    # Connection or other Redis errors
    print(f"Warning: Redis connection failed - {e}")
    redis_client = None