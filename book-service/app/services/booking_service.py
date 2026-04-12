from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.booking_dao import BookingDAO
from app.schemas.booking import BookingCreate
from app.core.kafka import kafka_manager

from app.core.logger import get_logger
from app.core.exceptions import BusinessLogicError

logger = get_logger("BOOKING_SERVICE")

class BookingService:
    @classmethod
    async def create_booking(cls, db: AsyncSession, book_id: int, user_id: int):
        logger.info(f"Пользователь {user_id} пытается забронировать книгу {book_id}")
        # 1. Формируем данные для создания (Pydantic провалидирует их)
        booking_in = BookingCreate(book_id=book_id, user_id=user_id)
        
        # 2. Пишем в базу
        new_booking = await BookingDAO.create(db, booking_in)
        await db.commit()
        
        # 3. Получаем полную информацию с книгой (через joinedload в DAO)
        full_booking = await BookingDAO.get_by_id(db, new_booking.id)
        
        if not full_booking:
            logger.error(f"Критический сбой: Бронь {new_booking.id} создана, но не найдена в БД")
            raise BusinessLogicError("Ошибка целостности данных после создания брони", status_code=500)

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
        
        logger.info(f"Бронь {full_booking.id} для книги '{full_booking.book.title}' успешно завершена")
        return full_booking