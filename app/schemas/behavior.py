from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class BehaviorCreate(BaseModel):
    event_type: str
    product_id: Optional[int] = None
    search_query: Optional[str] = None
    category: Optional[str] = None
    time_spent: Optional[float] = None


class BehaviorBatch(BaseModel):
    events: List[BehaviorCreate]


class BehaviorResponse(BaseModel):
    id: int
    user_id: int
    event_type: str
    product_id: Optional[int]
    search_query: Optional[str]
    category: Optional[str]
    time_spent: Optional[float]
    timestamp: datetime
    
    class Config:
        from_attributes = True