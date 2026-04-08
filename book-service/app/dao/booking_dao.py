from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.booking import Booking
from app.schemas.booking import BookingCreate

class BookingDAO:

    @classmethod
    async def get_all(cls, db: AsyncSession):
        stmt = select(Booking)
        result = await db.scalars(stmt)
        return result.all()
    
    @classmethod
    async def get_by_id(cls, db: AsyncSession, booking_id: int):
        return await db.get(Booking, booking_id)
    
    @classmethod
    async def create(cls, db: AsyncSession, booking_create: BookingCreate):
        new_booking = Booking(**booking_create.model_dump())
        
        db.add(new_booking)
        
        await db.commit()
        await db.refresh(new_booking)
        
        return new_booking

