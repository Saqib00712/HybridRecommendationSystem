from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse, ProductList
from app.services.product_service import (
    create_product, get_product, get_products,
    update_product, delete_product, search_products, get_total_products
)
from app.utils.security import get_current_user, get_current_admin_user

router = APIRouter()


@router.post("/", response_model=ProductResponse)
async def create_new_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin_user)
):
    """Create a new product (Admin only)"""
    return create_product(db, product_data)


@router.get("/", response_model=ProductList)
async def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all products with optional filters"""
    products = get_products(db, skip=skip, limit=limit, category=category, difficulty=difficulty)
    total = get_total_products(db)
    return ProductList(products=products, total=total)


@router.get("/search", response_model=ProductList)
async def search_products_endpoint(
    q: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Search products"""
    products = search_products(db, q, limit)
    return ProductList(products=products, total=len(products))


@router.get("/{product_id}", response_model=ProductResponse)
async def get_single_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Get a single product by ID"""
    return get_product(db, product_id)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_existing_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin_user)
):
    """Update a product (Admin only)"""
    return update_product(db, product_id, product_data)


@router.delete("/{product_id}")
async def delete_existing_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin_user)
):
    """Delete a product (Admin only)"""
    delete_product(db, product_id)
    return {"message": f"Product {product_id} deleted successfully"}