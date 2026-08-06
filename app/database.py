from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

from app.config import get_settings

settings = get_settings()

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Create engine
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Create SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


def get_db():
    """Dependency for getting database sessions"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    # Import all models here to ensure they are registered
    from app.models.user import User
    from app.models.product import Product
    from app.models.behavior import UserBehavior
    from app.models.recommendation import Recommendation
    
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")