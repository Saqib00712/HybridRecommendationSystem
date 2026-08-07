print('=== SMART RECO AI - SYSTEM CHECK ===')
print()

from app.database import SessionLocal
from app.models.user import User
from app.models.product import Product
from app.models.behavior import UserBehavior
from app.models.recommendation import Recommendation
from app.agents.recommendation_agent import run_recommendation_agent
from app.services.chroma_service import init_chroma, get_collection_count
from app.utils.mesh_api import generate_embedding
from app.utils.langsmith_config import langsmith_enabled
import asyncio

db = SessionLocal()

users = db.query(User).count()
products = db.query(Product).count()
behaviors = db.query(UserBehavior).count()
recs = db.query(Recommendation).count()
print(f'Users: {users} | Products: {products} | Behaviors: {behaviors} | Recs: {recs}')

time_events = db.query(UserBehavior).filter(UserBehavior.time_spent != None).count()
print(f'Time tracking events: {time_events}')

init_chroma()
print(f'ChromaDB: {get_collection_count()} docs')

loop = asyncio.new_event_loop()
emb = loop.run_until_complete(generate_embedding('test'))
loop.close()
print(f'Embeddings: {len(emb)} dims')

result = run_recommendation_agent(1, db)
print(f'Agent: {"OK" if result["success"] else "FAIL"} | {len(result["products"])} products | {result.get("execution_time")}')

print(f'LangSmith: {"ON" if langsmith_enabled else "OFF"}')

db.close()
print('\n=== DONE ===')