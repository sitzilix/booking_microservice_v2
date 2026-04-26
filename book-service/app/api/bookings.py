from fastapi import APIRouter, Depends, Header, status
from sqlalchemy.ext.asyncio import AsyncSession
from common.database import get_db
from app.schemas.booking import BookingResponse
from app.services.booking_service import BookingService
from common.dependencies import get_current_user_id

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post(
    "/{book_id}/book", 
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED
)
async def make_booking(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    # Эмулируем получение ID пользователя от Gateway/Auth сервиса
    x_user_id: int = Depends(get_current_user_id)
):
    return await BookingService.create_booking(db, book_id, x_user_id)