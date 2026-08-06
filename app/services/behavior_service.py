from sqlalchemy.orm import Session
from typing import List
from app.models.behavior import UserBehavior
from app.schemas.behavior import BehaviorCreate


def track_behavior(db: Session, user_id: int, behavior_data: BehaviorCreate) -> UserBehavior:
    """Track user behavior"""
    db_behavior = UserBehavior(
        user_id=user_id,
        event_type=behavior_data.event_type,
        product_id=behavior_data.product_id,
        search_query=behavior_data.search_query,
        category=behavior_data.category
    )
    
    db.add(db_behavior)
    db.commit()
    db.refresh(db_behavior)
    return db_behavior


def get_user_behaviors(db: Session, user_id: int, limit: int = 50) -> List[UserBehavior]:
    """Get user behaviors"""
    return db.query(UserBehavior).filter(
        UserBehavior.user_id == user_id
    ).order_by(UserBehavior.timestamp.desc()).limit(limit).all()


def get_recent_behaviors(db: Session, limit: int = 20) -> List[UserBehavior]:
    """Get recent behaviors across all users"""
    return db.query(UserBehavior).order_by(
        UserBehavior.timestamp.desc()
    ).limit(limit).all()


def should_generate_recommendation(db: Session, user_id: int) -> bool:
    """Check if user has enough activity for recommendation"""
    product_views = db.query(UserBehavior).filter(
        UserBehavior.user_id == user_id,
        UserBehavior.event_type == "product_view"
    ).count()
    
    searches = db.query(UserBehavior).filter(
        UserBehavior.user_id == user_id,
        UserBehavior.event_type == "search"
    ).count()
    
    return product_views >= 3 or searches >= 2