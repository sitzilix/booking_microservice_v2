from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.dao.book_dao import BookDAO
from app.dao.author_dao import AuthorDAO
from app.dao.genre_dao import GenreDAO
from app.schemas.book import BookCreate, BookResponse

class BookService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_books(self) -> list[BookResponse]:
        books = await BookDAO.get_all(self.db)
        return [BookResponse.model_validate(book) for book in books]

    async def get_book_by_id(self, book_id: int) -> BookResponse:
        book = await BookDAO.get_by_id(self.db, book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with ID {book_id} not found"
            )
        return BookResponse.model_validate(book)

    async def create_book(self, book_data: BookCreate) -> BookResponse:
        # 1. Проверяем, существует ли автор
        author = await AuthorDAO.get_by_id(self.db, book_data.author_id)
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Author with ID {book_data.author_id} not found"
            )

        # 2. Проверяем, существует ли жанр
        genre = await GenreDAO.get_by_id(self.db, book_data.genre_id)
        if not genre:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Genre with ID {book_data.genre_id} not found"
            )

        # 3. Если всё ок, создаем книгу
        new_book = await BookDAO.create(self.db, book_data)
        
        try:
            await self.db.commit()
            await self.db.refresh(new_book)
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create book"
            )
            
        return BookResponse.model_validate(new_book)