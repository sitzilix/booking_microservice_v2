from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.dao.genre_dao import GenreDAO
from app.schemas.genre import GenreCreate, GenreResponse

from app.core.logger import get_logger
from app.core.exceptions import BusinessLogicError

logger = get_logger("GENRE_SERVICE")

class GenreService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_genres(self) -> list[GenreResponse]:
        logger.info("Получение списка всех жанров")
        genres = await GenreDAO.get_all(self.db)
        return [GenreResponse.model_validate(genre) for genre in genres]
        
    async def get_genre_by_id(self, genre_id: int) -> GenreResponse:
        logger.info(f"Получение жанра с ID {genre_id}")
        genre = await GenreDAO.get_by_id(self.db, genre_id)
        if not genre:
            logger.warning(f"Жанр с ID {genre_id} не найден")
            raise BusinessLogicError(f"Жанр с ID {genre_id} не найден", status_code=404)
        
        return GenreResponse.model_validate(genre)
    
    async def create_genre(self, genre_data: GenreCreate) -> GenreResponse:
        logger.info(f"Создание нового жанра: {genre_data.name}")
        new_genre = await GenreDAO.create(self.db, genre_data)
    
        await self.db.commit()
        await self.db.refresh(new_genre)
        
        logger.info(f"Жанр {genre_data.name} успешно создан с ID {new_genre.id}")

    
        return GenreResponse.model_validate(new_genre)