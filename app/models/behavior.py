from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class UserBehavior(Base):
    __tablename__ = "user_behaviors"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    event_type = Column(String(50), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    search_query = Column(String(200), nullable=True)
    category = Column(String(100), nullable=True)
    time_spent = Column(Float, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())