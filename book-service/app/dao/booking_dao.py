from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.models.booking import Booking
from app.schemas.booking import BookingCreate

class BookingDAO:

    @classmethod
    async def get_all(cls, db: AsyncSession):
        stmt = select(Booking)
        result = await db.scalars(stmt)
        return result.all()
    
    @classmethod
    async def create(cls, db: AsyncSession, booking_data: BookingCreate) -> Booking:
        # model_dump() превращает схему в словарь, который распаковывается в модель
        new_booking = Booking(**booking_data.model_dump())
        db.add(new_booking)
        # Мы делаем flush, чтобы получить ID и created_at от БД до коммита
        await db.flush()
        return new_booking

    @classmethod
    async def get_by_id(cls, db: AsyncSession, booking_id: int):
        query = (
            select(Booking)
            .options(joinedload(Booking.book)) # Подгружаем книгу, чтобы избежать ошибки
            .filter(Booking.id == booking_id)
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()