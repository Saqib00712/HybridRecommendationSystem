from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BehaviorCreate(BaseModel):
    event_type: str  # "product_view", "search", "category_visit"
    product_id: Optional[int] = None
    search_query: Optional[str] = None
    category: Optional[str] = None


class BehaviorResponse(BaseModel):
    id: int
    user_id: int
    event_type: str
    product_id: Optional[int]
    search_query: Optional[str]
    category: Optional[str]
    timestamp: datetime
    
    class Config:
        from_attributes = True