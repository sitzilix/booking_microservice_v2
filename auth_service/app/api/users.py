from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.services.user_service import UserService
from common.database import get_db

router = APIRouter(
    prefix="/Users", 
    tags=["users"]
)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    return await service.register(user_in)

@router.post("/login")
async def login(user_in: UserLogin, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    return await service.login(user_in)