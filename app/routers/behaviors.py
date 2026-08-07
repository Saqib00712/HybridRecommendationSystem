from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.behavior import BehaviorCreate, BehaviorBatch, BehaviorResponse
from app.services.behavior_service import (
    track_behavior, track_behavior_batch, get_user_behaviors, should_generate_recommendation
)
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
    behavior = track_behavior(db, current_user.id, behavior_data)
    if should_generate_recommendation(db, current_user.id):
        try:
            result = run_recommendation_agent(current_user.id, db)
            if result["success"] and result["product_ids"]:
                save_recommendation(db, current_user.id, result["message"], result["product_ids"])
        except Exception as e:
            print(f"Auto-recommendation failed: {e}")
    return behavior


@router.post("/track-batch")
async def track_behavior_batch_endpoint(
    batch: BehaviorBatch,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    behaviors = track_behavior_batch(db, current_user.id, batch.events)
    if should_generate_recommendation(db, current_user.id):
        try:
            result = run_recommendation_agent(current_user.id, db)
            if result["success"] and result["product_ids"]:
                save_recommendation(db, current_user.id, result["message"], result["product_ids"])
        except Exception as e:
            print(f"Auto-recommendation failed: {e}")
    return {"tracked": len(behaviors), "message": f"Batch of {len(behaviors)} events tracked"}


@router.get("/my", response_model=List[BehaviorResponse])
async def get_my_behaviors(limit: int = 50, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_user_behaviors(db, current_user.id, limit)


@router.get("/check-recommendation")
async def check_if_should_recommend(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    should = should_generate_recommendation(db, current_user.id)
    return {"should_generate_recommendation": should}
    
