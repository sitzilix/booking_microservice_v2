from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.dao.genre_dao import GenreDAO
from app.schemas.genre import GenreCreate, GenreResponse

class GenreService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_genres(self) -> list[GenreResponse]:
        genres = await GenreDAO.get_all(self.db)
        return [GenreResponse.model_validate(genre) for genre in genres]
        
    async def get_genre_by_id(self, genre_id: int) -> GenreResponse:
        genre = await GenreDAO.get_by_id(self.db, genre_id)
        if not genre:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Genre with ID {genre_id} not found"
            )
        return GenreResponse.model_validate(genre)
    
    async def create_genre(self, genre_data: GenreCreate) -> GenreResponse:
        new_genre = await GenreDAO.create(self.db, genre_data)
        
        try:
            await self.db.commit()
            await self.db.refresh(new_genre)
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=f"Failed to create genre: {str(e)}"
            )
    
        return GenreResponse.model_validate(new_genre)