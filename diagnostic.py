"""
SmartReco AI - Complete System Diagnostic
"""
print("=" * 60)
print("🔍 SmartReco AI - System Diagnostic")
print("=" * 60)

errors = []
warnings = []

# 1. Check imports
print("\n📦 Checking imports...")
try:
    from app.config import get_settings
    settings = get_settings()
    print("✅ Config loaded")
except Exception as e:
    errors.append(f"Config: {e}")

try:
    from app.database import SessionLocal, init_db
    init_db()
    print("✅ Database initialized")
except Exception as e:
    errors.append(f"Database: {e}")

try:
    from app.services.chroma_service import init_chroma, get_collection_count
    init_chroma()
    count = get_collection_count()
    print(f"✅ ChromaDB: {count} documents")
    if count < 50:
        warnings.append(f"ChromaDB has only {count} docs (expected 50)")
except Exception as e:
    errors.append(f"ChromaDB: {e}")

try:
    from app.utils.mesh_api import generate_embedding, generate_recommendation_message
    import asyncio
    loop = asyncio.new_event_loop()
    emb = loop.run_until_complete(generate_embedding("test"))
    loop.close()
    print(f"✅ Embeddings: {len(emb)} dimensions")
except Exception as e:
    errors.append(f"Embeddings: {e}")

try:
    from app.agents.recommendation_agent import run_recommendation_agent
    print("✅ Agent imported")
except Exception as e:
    errors.append(f"Agent: {e}")

# 2. Check database
print("\n📊 Checking database...")
db = SessionLocal()

from app.models.user import User
from app.models.product import Product
from app.models.behavior import UserBehavior
from app.models.recommendation import Recommendation

users = db.query(User).count()
products = db.query(Product).count()
behaviors = db.query(UserBehavior).count()
recommendations = db.query(Recommendation).count()

print(f"✅ Users: {users}")
print(f"✅ Products: {products}")
print(f"✅ Behaviors: {behaviors}")
print(f"✅ Recommendations: {recommendations}")

if users < 2:
    warnings.append("Less than 2 users (admin + user needed)")
if products < 50:
    warnings.append(f"Only {products} products (50 expected)")
if behaviors < 1:
    warnings.append("No user behavior data")

# 3. Check product fields
print("\n📦 Checking product data...")
sample = db.query(Product).first()
if sample:
    fields = ['title', 'description', 'category', 'difficulty', 'price', 'instructor', 'duration', 'tags']
    for field in fields:
        val = getattr(sample, field, None)
        if val is None or val == '':
            warnings.append(f"Product #{sample.id}: '{field}' is empty")
    print(f"✅ Sample product #{sample.id}: {sample.title}")
    print(f"   Instructor: {sample.instructor}")
    print(f"   chroma_id: {sample.chroma_id}")

# 4. Test recommendation
print("\n🤖 Testing recommendation agent...")
try:
    result = run_recommendation_agent(1, db)
    if result["success"]:
        print(f"✅ Agent works: {len(result['products'])} products recommended")
        print(f"   Execution time: {result.get('execution_time', 'N/A')}")
    else:
        errors.append(f"Agent failed: {result['message']}")
except Exception as e:
    errors.append(f"Agent error: {e}")

# 5. Check ChromaDB sync
print("\n🔗 Checking dual-write sync...")
products_with_chroma = db.query(Product).filter(Product.chroma_id.isnot(None)).count()
print(f"✅ Products with chroma_id: {products_with_chroma}/{products}")
if products_with_chroma < products:
    warnings.append(f"{products - products_with_chroma} products missing chroma_id")

db.close()

# 6. Check files
import os
print("\n📁 Checking project files...")
required_files = [
    'app/main.py', 'app/config.py', 'app/database.py',
    'app/models/user.py', 'app/models/product.py',
    'app/routers/auth.py', 'app/routers/products.py',
    'app/routers/behaviors.py', 'app/routers/recommendations.py',
    'app/routers/pages.py',
    'app/agents/recommendation_agent.py',
    'app/utils/security.py', 'app/utils/mesh_api.py',
    'app/utils/langsmith_config.py',
    'app/templates/base.html',
    'app/templates/user/dashboard.html',
    'app/templates/user/products.html',
    'app/templates/admin/dashboard.html',
    'app/templates/admin/products.html',
    'app/templates/auth/login.html',
    'requirements.txt', '.env', '.gitignore', 'README.md'
]

for file in required_files:
    if os.path.exists(file):
        pass  # OK
    else:
        errors.append(f"Missing file: {file}")
print(f"✅ Checked {len(required_files)} required files")

# Summary
print("\n" + "=" * 60)
print("📋 DIAGNOSTIC SUMMARY")
print("=" * 60)

if errors:
    print(f"\n❌ ERRORS ({len(errors)}):")
    for e in errors:
        print(f"   • {e}")
else:
    print("\n✅ No critical errors!")

if warnings:
    print(f"\n⚠️ WARNINGS ({len(warnings)}):")
    for w in warnings:
        print(f"   • {w}")
else:
    print("\n✅ No warnings!")

print("\n" + "=" * 60)
if not errors:
    print("🎉 SYSTEM IS HEALTHY!")
else:
    print("🔧 Fix the errors above before submitting!")
print("=" * 60)