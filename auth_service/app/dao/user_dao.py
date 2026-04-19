from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User

class UserDAO:
    @classmethod
    async def get_by_email(cls, db: AsyncSession, email: str):
        query = select(User).filter(User.email == email)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    @classmethod
    async def create_user(cls, db: AsyncSession, email: str, hashed_password: str):
        db_user = User(
            email=email,
            hashed_password=hashed_password
        )
        db.add(db_user)
        
        return db_user