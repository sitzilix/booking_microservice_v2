from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.genre import GenreCreate, GenreResponse
from app.services.genre_service import GenreService
from common.database import get_db

router = APIRouter(
    prefix="/genres",
    tags=["genres"]
)

@router.get("/", response_model=list[GenreResponse])
async def get_genres(db: AsyncSession = Depends(get_db)):
    service = GenreService(db)
    return await service.get_all_genres()

@router.post("/", response_model=GenreResponse)
async def create_genre(genre: GenreCreate, db: AsyncSession = Depends(get_db)):
    service = GenreService(db)
    return await service.create_genre(genre)

@router.get("/{genre_id}", response_model=GenreResponse)
async def get_genre(genre_id: int, db: AsyncSession = Depends(get_db)):
    service = GenreService(db)
    return await service.get_genre_by_id(genre_id)
