from app.database import SessionLocal
from app.services.behavior_service import track_behavior
from app.schemas.behavior import BehaviorCreate
from app.models.user import User

db = SessionLocal()
user = db.query(User).filter(User.username == 'user').first()

if user:
    # Track product views
    for pid in [1, 2, 3]:
        behavior = BehaviorCreate(event_type='product_view', product_id=pid)
        track_behavior(db, user.id, behavior)
        print(f'✅ Tracked product view: {pid}')
    
    # Track search
    behavior = BehaviorCreate(event_type='search', search_query='Python AI')
    track_behavior(db, user.id, behavior)
    print('✅ Tracked search')
    
    # Check recommendation trigger
    from app.services.behavior_service import should_generate_recommendation
    should = should_generate_recommendation(db, user.id)
    print(f'Should generate recommendation: {should}')

db.close()
print('✅ Done!')