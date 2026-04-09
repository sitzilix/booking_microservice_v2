from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.models.book import Book
from app.schemas.book import BookCreate

class BookDAO:
    @classmethod
    async def get_all(cls, db: AsyncSession):
        query = (
        select(Book)
            .options(
                joinedload(Book.author), # Подгружаем автора сразу
                joinedload(Book.genre)   # Подгружаем жанр сразу
            )
        )
        result = await db.scalars(query)
        return result.all()

    @classmethod
    async def get_by_id(cls, db: AsyncSession, book_id: int):
        # Используем select с теми же опциями, что и в get_all
        query = (
            select(Book)
            .options(
                joinedload(Book.author),
                joinedload(Book.genre)
            )
            .filter(Book.id == book_id)
        )
        result = await db.execute(query)
        return result.scalar_one_or_none() # Вернет книгу или None, если id нет

    @classmethod
    async def create(cls, db: AsyncSession, book_create: BookCreate):
        new_book = Book(**book_create.model_dump())
        
        db.add(new_book)
                
        return new_book