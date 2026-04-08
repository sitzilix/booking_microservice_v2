from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.book import Book
from app.schemas.book import BookCreate

class BookDAO:
    @classmethod
    async def get_all(cls, db: AsyncSession):
        stmt = select(Book)
        result = await db.scalars(stmt)
        return result.all()

    @classmethod
    async def get_by_id(cls, db: AsyncSession, book_id: int):
        return await db.get(Book, book_id)

    @classmethod
    async def create(cls, db: AsyncSession, book_create: BookCreate):
        new_book = Book(**book_create.model_dump())
        
        db.add(new_book)
                
        return new_book