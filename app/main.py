from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.config import get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print(f"🚀 Starting {settings.app_name}...")
    
    # Initialize database
    from app.database import init_db
    init_db()
    
    # Initialize ChromaDB
    try:
        from app.services.chroma_service import init_chroma
        init_chroma()
        print("✅ ChromaDB initialized!")
    except Exception as e:
        print(f"⚠️ ChromaDB initialization skipped: {e}")
    
    print(f"✅ {settings.app_name} is ready!")
    yield
    
    # Shutdown
    print(f"👋 Shutting down {settings.app_name}...")


# Import all routers
from app.routers import auth, products, behaviors, recommendations, pages

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include all routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(behaviors.router, prefix="/api/behaviors", tags=["Behaviors"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["Recommendations"])
app.include_router(pages.router, tags=["Pages"])


@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}