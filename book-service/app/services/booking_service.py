from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.booking_dao import BookingDAO
from app.schemas.booking import BookingCreate
from app.core.kafka import kafka_manager

class BookingService:
    @classmethod
    async def create_booking(cls, db: AsyncSession, book_id: int, user_id: int):
        # 1. Формируем данные для создания (Pydantic провалидирует их)
        booking_in = BookingCreate(book_id=book_id, user_id=user_id)
        
        try:
            # 2. Пишем в базу
            new_booking = await BookingDAO.create(db, booking_in)
            await db.commit()
            
            # 3. Получаем полную информацию с книгой (через joinedload в DAO)
            full_booking = await BookingDAO.get_by_id(db, new_booking.id)
            
            if not full_booking:
                raise HTTPException(status_code=404, detail="Ошибка после создания брони")

            # 4. Отправляем событие в Kafka
            event_data = {
                "booking_id": full_booking.id,
                "user_id": full_booking.user_id,
                "book_title": full_booking.book.title,
                "status": full_booking.status,
                "created_at": str(full_booking.created_at)
            }
            
            # Топик должен совпадать с тем, что будет слушать Notification Service
            await kafka_manager.send_event("booking_created", event_data)
            
            return full_booking

        except Exception as e:
            await db.rollback()
            print(f"Ошибка при бронировании: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Не удалось оформить бронирование"
            )