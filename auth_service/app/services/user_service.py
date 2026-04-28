import json

from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate, UserLogin
from app.dao.user_dao import UserDAO

from common.config import settings

from app.core.security import create_access_token, pwd_context
from app.core.redis import redis_client



class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _check_rate_limit(self, key: str, limit: int, window: int):
        current = await redis_client.incr(key)
        if current == 1:
            await redis_client.expire(key, window)
        if current > limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Слишком много попыток. Попробуйте через {window} секунд"
            )
            
    async def _cache_user_profile(self, user):
        cache_key = f"user:profile:{user.id}"
        user_data = {
            "id": user.id,
            "email": user.email
        }
        await redis_client.setex(
            cache_key,
            3600,
            json.dumps(user_data)
        )

    async def register(self, user_in: UserCreate):
        await self._check_rate_limit(f"rate:reg:{user_in.email}", limit=3, window=3600)
        
        user = await UserDAO.get_by_email(self.db, user_in.email)
        if user:
            raise HTTPException(status_code=400, detail="Пользователь уже зарегистрирован")

        hashed_pwd = pwd_context.hash(user_in.password)
        new_user = await UserDAO.create_user(self.db, email=user_in.email, hashed_password=hashed_pwd)
        
        await self.db.commit()
        await self.db.refresh(new_user)
        
        await self._cache_user_profile(new_user)
        
        return new_user
    
    async def login(self, user_in: UserLogin):
        await self._check_rate_limit(f"rate:login:{user_in.email}", limit=5, window=3600)
        
        user = await UserDAO.get_by_email(self.db, user_in.email)
        
        if not user or not pwd_context.verify(user_in.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        access_token = create_access_token(data={"sub": str(user.id), "email": user.email, "type": "access"})
        refresh_token = create_access_token(data={"sub": str(user.id), "email": user.email, "type": "refresh"})

        redis_expire_seconds = settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        await redis_client.set(
            name=f"refresh_token:{user.id}",
            value=refresh_token,
            ex=redis_expire_seconds
        )
        
        await self._cache_user_profile(user)
        
        await redis_client.delete(f"rate:login:{user_in.email}")
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
        