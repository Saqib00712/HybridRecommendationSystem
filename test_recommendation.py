import sys
print("Starting test...", flush=True)

try:
    from app.database import SessionLocal
    print("Imported database", flush=True)
    
    from app.agents.recommendation_agent import run_recommendation_agent
    print("Imported agent", flush=True)
    
    db = SessionLocal()
    print("Connected to DB", flush=True)
    
    result = run_recommendation_agent(2, db)
    print("Agent ran!", flush=True)
    
    print("\n" + "="*50, flush=True)
    print(f"Success: {result['success']}", flush=True)
    print(f"Message: {result['message']}", flush=True)
    print(f"Interests: {result['interests']}", flush=True)
    print(f"Product IDs: {result['product_ids']}", flush=True)
    print("="*50, flush=True)
    
    db.close()
    
except Exception as e:
    print(f"ERROR: {e}", flush=True)
    import traceback
    traceback.print_exc()