from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.author import Author
from app.schemas.author import AuthorCreate 

class AuthorDAO:
    
    @classmethod
    async def get_all(cls, db: AsyncSession):
        stmt = select(Author)
        result = await db.scalars(stmt)
        return result.all()
    
    @classmethod
    async def get_by_id(cls, db: AsyncSession, author_id: int):
        return await db.get(Author, author_id)
    
    @classmethod
    async def create(cls, db: AsyncSession, author_create: AuthorCreate):
        new_author = Author(**author_create.model_dump())
        
        db.add(new_author)
                
        return new_author