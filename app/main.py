from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.config import get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"🚀 Starting {settings.app_name}...")
    
    from app.database import init_db
    init_db()
    
    try:
        from app.services.chroma_service import init_chroma
        init_chroma()
        print("✅ ChromaDB initialized!")
    except Exception as e:
        print(f"⚠️ ChromaDB: {e}")
    
    try:
        from app.services.scheduler_service import start_scheduler
        start_scheduler()
    except Exception as e:
        print(f"⚠️ Scheduler: {e}")
    
    print(f"✅ {settings.app_name} is ready!")
    yield
    print(f"👋 Shutting down...")


from app.routers import auth, products, behaviors, recommendations, pages

app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan, docs_url="/docs", redoc_url="/redoc")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(behaviors.router, prefix="/api/behaviors", tags=["Behaviors"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["Recommendations"])
app.include_router(pages.router, tags=["Pages"])


@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.app_name}", "version": "1.0.0", "docs": "/docs"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}