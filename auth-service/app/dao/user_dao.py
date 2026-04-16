from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from app.models.user import User
from app.schemas.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserDAO:
    @classmethod
    async def get_by_email(cls, db: AsyncSession, email: str):
        query = select(User).filter(User.email == email)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    @classmethod
    async def create_user(cls, db: AsyncSession, user_in: UserCreate):
        hashed_password = pwd_context.hash(user_in.password)
        
        db_user = User(
            email=user_in.email,
            hashed_password=hashed_password
        )
        db.add(db_user)
        
        return db_user