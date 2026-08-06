from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.behavior import BehaviorCreate, BehaviorResponse
from app.services.behavior_service import track_behavior, get_user_behaviors, should_generate_recommendation
from app.agents.recommendation_agent import run_recommendation_agent
from app.services.recommendation_service import save_recommendation
from app.utils.security import get_current_user

router = APIRouter()


@router.post("/track", response_model=BehaviorResponse)
async def track_user_behavior(
    behavior_data: BehaviorCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Track a user behavior event and auto-generate recommendation"""
    behavior = track_behavior(db, current_user.id, behavior_data)
    
    # ALWAYS generate recommendation when user views a product or searches
    if behavior_data.event_type in ["product_view", "search"]:
        try:
            result = run_recommendation_agent(current_user.id, db)
            if result["success"] and result["product_ids"]:
                save_recommendation(db, current_user.id, result["message"], result["product_ids"])
                print(f"✅ Generated recommendation for user {current_user.id}")
        except Exception as e:
            print(f"Auto-recommendation failed: {e}")
    
    return behavior


@router.get("/my", response_model=List[BehaviorResponse])
async def get_my_behaviors(
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Get current user's behaviors"""
    return get_user_behaviors(db, current_user.id, limit)


@router.get("/check-recommendation")
async def check_if_should_recommend(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Check if user has enough activity for recommendation"""
    should_recommend = should_generate_recommendation(db, current_user.id)
    return {
        "should_generate_recommendation": should_recommend,
        "message": "You have enough activity for recommendations!" if should_recommend else "Keep exploring! View 3 products or search 2 times."
    }