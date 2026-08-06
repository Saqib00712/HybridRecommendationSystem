from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./data/smartreco.db"
    
    # JWT
    secret_key: str = "smartreco-ai-secret-key-2026-hackathon"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    
    # ChromaDB
    chroma_persist_directory: str = "./data/chroma_db"
    
    # Mesh API
    mesh_api_key: str = ""
    mesh_api_url: str = "https://api.meshapi.ai/v1"
    mesh_model: str = "tencent/hy3"
    
    # LangSmith
    langsmith_api_key: str = ""
    langsmith_project: str = "smartreco-ai"
    langsmith_endpoint: str = "https://api.smith.langchain.com"
    
    # App
    app_name: str = "SmartReco AI"
    debug: bool = True
    
    class Config:
        env_file = ".env"
        extra = "allow"  # ADD THIS LINE - allows extra fields from .env


@lru_cache()
def get_settings():
    return Settings()