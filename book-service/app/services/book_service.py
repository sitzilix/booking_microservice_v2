from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.book_dao import BookDAO
from app.dao.author_dao import AuthorDAO
from app.dao.genre_dao import GenreDAO
from app.schemas.book import BookCreate, BookResponse
from app.core.logger import get_logger
from app.core.exceptions import BusinessLogicError


logger = get_logger("BOOK_SERVICE")

class BookService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_books(self) -> list[BookResponse]:
        logger.info("Запрос списка всех книг")
        books = await BookDAO.get_all(self.db)
        return [BookResponse.model_validate(book) for book in books]

    async def get_book_by_id(self, book_id: int) -> BookResponse:
        logger.info(f"Запрос книги с ID {book_id}")
        book = await BookDAO.get_by_id(self.db, book_id)
        if not book:
            logger.warning(f"Book with ID {book_id} not found")
            raise BusinessLogicError(f"Book with ID {book_id} not found")
        return BookResponse.model_validate(book)

    async def create_book(self, book_data: BookCreate) -> BookResponse:
        logger.info(f"Создание новой книги: {book_data.title}")
        # 1. Проверяем, существует ли автор
        author = await AuthorDAO.get_by_id(self.db, book_data.author_id)
        if not author:
            logger.warning(f"Автор с ID {book_data.author_id} not found")
            raise BusinessLogicError(f"Автор с ID {book_data.author_id} не найден")
        # 2. Проверяем, существует ли жанр
        genre = await GenreDAO.get_by_id(self.db, book_data.genre_id)
        if not genre:
            logger.warning(f"Жанр с ID {book_data.genre_id} not found")
            raise BusinessLogicError(f"Жанр с ID {book_data.genre_id} не найден")

        # 3. Если всё ок, создаем книгу
        new_book = await BookDAO.create(self.db, book_data)
        

        await self.db.commit()
        await self.db.refresh(new_book)
        
        logger.info(f"Книга {book_data.title} успешно создана с ID {new_book.id}")
            
        return BookResponse.model_validate(new_book)