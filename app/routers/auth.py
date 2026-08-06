from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.auth_service import create_user, authenticate_user
from app.utils.security import create_access_token, get_current_user
from app.config import get_settings

settings = get_settings()
router = APIRouter()


@router.post("/register", response_model=Token)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    user = create_user(db, user_data)
    
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
    )
    
    return Token(
        access_token=access_token,
        user=UserResponse.from_orm(user)
    )


@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    user = authenticate_user(db, user_data.username, user_data.password)
    
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
    )
    
    return Token(
        access_token=access_token,
        user=UserResponse.from_orm(user)
    )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user=Depends(get_current_user)):
    """Get current user info"""
    return UserResponse.from_orm(current_user)