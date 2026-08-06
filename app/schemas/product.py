from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ProductBase(BaseModel):
    title: str
    description: str
    category: str
    difficulty: str
    price: float = 0.0
    instructor: str
    duration: str
    tags: str
    thumbnail: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    difficulty: Optional[str] = None
    price: Optional[float] = None
    instructor: Optional[str] = None
    duration: Optional[str] = None
    tags: Optional[str] = None
    thumbnail: Optional[str] = None


class ProductResponse(ProductBase):
    id: int
    chroma_id: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class ProductList(BaseModel):
    products: List[ProductResponse]
    total: int