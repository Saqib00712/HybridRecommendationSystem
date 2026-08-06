from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)
    difficulty = Column(String(50), nullable=False)  # Beginner, Intermediate, Advanced
    price = Column(Float, default=0.0)
    instructor = Column(String(100), nullable=False)
    duration = Column(String(50), nullable=False)  # e.g., "8 weeks", "3 hours"
    tags = Column(String(500), nullable=False)  # Comma-separated tags
    thumbnail = Column(String(500), nullable=True)  # URL or path to thumbnail
    chroma_id = Column(String(200), nullable=True)  # ID in ChromaDB for dual write
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())