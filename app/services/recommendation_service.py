from sqlalchemy.orm import Session
from typing import List, Dict, Any
import json
from app.models.recommendation import Recommendation


def save_recommendation(
    db: Session,
    user_id: int,
    message: str,
    product_ids: List[int]
) -> Recommendation:
    """Save a recommendation to database"""
    db_recommendation = Recommendation(
        user_id=user_id,
        generated_message=message,
        recommended_products=json.dumps(product_ids)
    )
    
    db.add(db_recommendation)
    db.commit()
    db.refresh(db_recommendation)
    
    return db_recommendation


def get_latest_recommendation(db: Session, user_id: int) -> Recommendation:
    """Get the latest recommendation for a user"""
    return db.query(Recommendation).filter(
        Recommendation.user_id == user_id
    ).order_by(Recommendation.timestamp.desc()).first()


def get_user_recommendations(db: Session, user_id: int, limit: int = 10) -> List[Recommendation]:
    """Get recommendation history for a user"""
    return db.query(Recommendation).filter(
        Recommendation.user_id == user_id
    ).order_by(Recommendation.timestamp.desc()).limit(limit).all()


def get_total_recommendations(db: Session) -> int:
    """Get total number of recommendations"""
    return db.query(Recommendation).count()