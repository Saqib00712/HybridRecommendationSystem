from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class Recommendation(Base):
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    generated_message = Column(Text, nullable=False)
    recommended_products = Column(Text, nullable=False)  # JSON string of product IDs
    timestamp = Column(DateTime(timezone=True), server_default=func.now())