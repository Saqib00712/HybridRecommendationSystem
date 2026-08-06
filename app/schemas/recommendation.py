from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class RecommendationResponse(BaseModel):
    id: int
    user_id: int
    generated_message: str
    recommended_products: str  # JSON string
    timestamp: datetime
    
    class Config:
        from_attributes = True


class RecommendationWithProducts(BaseModel):
    recommendation: Optional[RecommendationResponse] = None
    products: List[dict] = []