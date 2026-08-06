from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.recommendation import RecommendationResponse, RecommendationWithProducts
from app.services.recommendation_service import (
    save_recommendation, get_latest_recommendation, 
    get_user_recommendations
)
from app.agents.recommendation_agent import run_recommendation_agent
from app.utils.security import get_current_user
from app.models.product import Product
import json

router = APIRouter()


@router.post("/generate")
async def generate_recommendation(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Generate a new recommendation for the current user"""
    
    # Run the AI agent
    result = run_recommendation_agent(current_user.id, db)
    
    if result["success"] and result["product_ids"]:
        # Save to database
        recommendation = save_recommendation(
            db, 
            current_user.id, 
            result["message"], 
            result["product_ids"]
        )
        
        # Get full product details
        products = []
        for pid in result["product_ids"]:
            product = db.query(Product).filter(Product.id == pid).first()
            if product:
                products.append({
                    "id": product.id,
                    "title": product.title,
                    "category": product.category,
                    "description": product.description,
                    "difficulty": product.difficulty,
                    "price": product.price,
                    "instructor": product.instructor,
                    "duration": product.duration
                })
        
        return {
            "recommendation": RecommendationResponse.from_orm(recommendation),
            "products": products,
            "interests": result["interests"]
        }
    
    return {
        "message": result["message"],
        "products": [],
        "interests": result["interests"]
    }


@router.get("/latest", response_model=RecommendationWithProducts)
async def get_latest(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Get latest recommendation for current user"""
    recommendation = get_latest_recommendation(db, current_user.id)
    
    if not recommendation:
        return {"recommendation": None, "products": []}
    
    # Get products
    product_ids = json.loads(recommendation.recommended_products)
    products = []
    for pid in product_ids:
        product = db.query(Product).filter(Product.id == pid).first()
        if product:
            products.append({
                "id": product.id,
                "title": product.title,
                "category": product.category,
                "description": product.description,
                "difficulty": product.difficulty,
                "price": product.price
            })
    
    return {
        "recommendation": RecommendationResponse.from_orm(recommendation),
        "products": products
    }


@router.get("/history", response_model=List[RecommendationResponse])
async def get_history(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Get recommendation history"""
    return get_user_recommendations(db, current_user.id, limit)