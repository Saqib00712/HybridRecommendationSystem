from sqlalchemy.orm import Session
from typing import List
from app.models.behavior import UserBehavior
from app.schemas.behavior import BehaviorCreate


def track_behavior(db: Session, user_id: int, behavior_data: BehaviorCreate) -> UserBehavior:
    db_behavior = UserBehavior(
        user_id=user_id,
        event_type=behavior_data.event_type,
        product_id=behavior_data.product_id,
        search_query=behavior_data.search_query,
        category=behavior_data.category,
        time_spent=behavior_data.time_spent
    )
    db.add(db_behavior)
    db.commit()
    db.refresh(db_behavior)
    return db_behavior


def track_behavior_batch(db: Session, user_id: int, events: List[BehaviorCreate]) -> List[UserBehavior]:
    behaviors = []
    for event in events:
        db_behavior = UserBehavior(
            user_id=user_id,
            event_type=event.event_type,
            product_id=event.product_id,
            search_query=event.search_query,
            category=event.category,
            time_spent=event.time_spent
        )
        db.add(db_behavior)
        behaviors.append(db_behavior)
    db.commit()
    return behaviors


def get_user_behaviors(db: Session, user_id: int, limit: int = 50) -> List[UserBehavior]:
    return db.query(UserBehavior).filter(
        UserBehavior.user_id == user_id
    ).order_by(UserBehavior.timestamp.desc()).limit(limit).all()


def should_generate_recommendation(db: Session, user_id: int) -> bool:
    product_views = db.query(UserBehavior).filter(
        UserBehavior.user_id == user_id,
        UserBehavior.event_type == "product_view"
    ).count()
    searches = db.query(UserBehavior).filter(
        UserBehavior.user_id == user_id,
        UserBehavior.event_type == "search"
    ).count()
    return product_views >= 3 or searches >= 2