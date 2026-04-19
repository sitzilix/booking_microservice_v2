from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserLogin
from app.dao.user_dao import UserDAO
from common.database import get_db
from app.core.security import create_access_token, pwd_context



class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register(self, user_in: UserCreate):
        user = await UserDAO.get_by_email(self.db, user_in.email)
        if user:
            raise HTTPException(status_code=400, detail="Пользователь уже зарегистрирован")

        hashed_pwd = pwd_context.hash(user_in.password)
        new_user = await UserDAO.create_user(self.db, email=user_in.email, hashed_password=hashed_pwd)
        
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user
    
    async def login(self, user_in: UserLogin):
        user = await UserDAO.get_by_email(self.db, user_in.email)
        
        if not user or not pwd_context.verify(user_in.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        access_token = create_access_token(data={"sub": str(user.id), "email": user.email})
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
        