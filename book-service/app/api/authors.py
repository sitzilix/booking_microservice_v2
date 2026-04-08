from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.author import AuthorCreate, AuthorResponse
from app.services.author_service import AuthorService
from app.database import get_db

router = APIRouter(
    prefix="/authors", 
    tags=["authors"]
)
    
@router.get("/", response_model=list[AuthorResponse])
async def get_authors(db: AsyncSession = Depends(get_db)):
    service = AuthorService(db)
    return await service.get_all_authors()

@router.post("/", response_model=AuthorResponse)
async def create_author(author: AuthorCreate, db: AsyncSession = Depends(get_db)):
    service = AuthorService(db)
    return await service.create_author(author)

@router.get("/{author_id}", response_model=AuthorResponse)
async def get_author(author_id: int, db: AsyncSession = Depends(get_db)):
    service = AuthorService(db)
    return await service.get_author_by_id(author_id)