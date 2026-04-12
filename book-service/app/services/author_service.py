from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.author_dao import AuthorDAO
from app.schemas.author import AuthorCreate, AuthorResponse
from app.core.logger import get_logger
from app.core.exceptions import BusinessLogicError

logger = get_logger("AUTHOR_SERVICE")

class AuthorService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_authors(self) -> list[AuthorResponse]:
        logger.info("Запрос списка всех авторов")
        authors = await AuthorDAO.get_all(self.db)
        return [AuthorResponse.model_validate(author) for author in authors]
        
    async def get_author_by_id(self, author_id: int) -> AuthorResponse:
        author = await AuthorDAO.get_by_id(self.db, author_id)
        if not author:
            logger.warning(f"Автор с ID {author_id} не найден")
            raise BusinessLogicError(f"Автор с ID {author_id} не найден")
    
        return AuthorResponse.model_validate(author)
        
    async def create_author(self, author_data: AuthorCreate) -> AuthorResponse:
        logger.info(f"Создание нового автора: {author_data.name}")
        new_author = await AuthorDAO.create(self.db, author_data)
        
        await self.db.commit()
        await self.db.refresh(new_author)
        
        logger.info(f"Автор {author_data.name} успешно создан с ID {new_author.id}")
    
        return AuthorResponse.model_validate(new_author)