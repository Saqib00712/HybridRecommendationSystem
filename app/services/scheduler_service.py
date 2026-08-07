"""
APScheduler - Daily Recommendation Digest
"""
from apscheduler.schedulers.background import BackgroundScheduler
from app.database import SessionLocal
from app.models.user import User
from app.agents.recommendation_agent import run_recommendation_agent
from app.services.email_service import send_daily_digest

scheduler = BackgroundScheduler()


def send_digest_to_all_users():
    """Send daily digest to all active users"""
    print("🔄 [Scheduler] Starting daily digest...")
    db = SessionLocal()
    users = db.query(User).filter(User.is_active == True).all()
    sent = 0
    
    for user in users:
        try:
            result = run_recommendation_agent(user.id, db)
            if result["success"] and result["products"]:
                success = send_daily_digest(
                    user_email=user.email,
                    user_name=user.full_name or user.username,
                    message=result["message"],
                    products=result["products"]
                )
                if success: sent += 1
        except Exception as e:
            print(f"Digest failed for {user.email}: {e}")
    
    db.close()
    print(f"✅ [Scheduler] Complete! Sent to {sent}/{len(users)} users")


def start_scheduler():
    """Start background scheduler"""
    scheduler.add_job(send_digest_to_all_users, 'cron', hour=15, minute=0)
    scheduler.start()
    print("✅ [Scheduler] Started - Daily digest at 3:00 PM UTC")