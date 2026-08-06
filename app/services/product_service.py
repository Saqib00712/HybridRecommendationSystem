from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def create_product(db: Session, product_data: ProductCreate) -> Product:
    """Create a new product"""
    db_product = Product(**product_data.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product(db: Session, product_id: int) -> Product:
    """Get a single product by ID"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product


def get_products(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    category: Optional[str] = None,
    difficulty: Optional[str] = None
) -> List[Product]:
    """Get products with optional filters"""
    query = db.query(Product)
    
    if category:
        query = query.filter(Product.category == category)
    if difficulty:
        query = query.filter(Product.difficulty == difficulty)
    
    return query.offset(skip).limit(limit).all()


def update_product(db: Session, product_id: int, product_data: ProductUpdate) -> Product:
    """Update a product"""
    product = get_product(db, product_id)
    
    update_data = product_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int):
    """Delete a product"""
    product = get_product(db, product_id)
    db.delete(product)
    db.commit()


def get_total_products(db: Session) -> int:
    """Get total number of products"""
    return db.query(Product).count()


def search_products(db: Session, query: str, limit: int = 10) -> List[Product]:
    """Search products by title or description"""
    search = f"%{query}%"
    return db.query(Product).filter(
        (Product.title.ilike(search)) | 
        (Product.description.ilike(search)) |
        (Product.tags.ilike(search))
    ).limit(limit).all()