from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.book import BookCreate, BookResponse
from app.services.book_service import BookService
from app.database import get_db

router = APIRouter(
    prefix="/books",
    tags=["books"]
)

@router.get("/", response_model=list[BookResponse])
async def get_books(db: AsyncSession = Depends(get_db)):
    service = BookService(db)
    return await service.get_all_books()

@router.post("/", response_model=BookResponse)
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    service = BookService(db)
    return await service.create_book(book)

@router.get("/{book_id}", response_model=BookResponse)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    service = BookService(db)
    return await service.get_book_by_id(book_id)
