from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.genre import Genre
from app.schemas.genre import GenreCreate

class GenreDAO:
    @classmethod 
    async def get_all(cls, db: AsyncSession):
        stmt = select(Genre)
        result = await db.scalars(stmt)
        return result.all()
    
    @classmethod
    async def get_by_id(cls, db: AsyncSession, genre_id: int):
        return await db.get(Genre, genre_id)
    
    @classmethod
    async def create(cls, db: AsyncSession, genre_create: GenreCreate):
        new_genre = Genre(**genre_create.model_dump())
        
        db.add(new_genre)
        
        return new_genre
    