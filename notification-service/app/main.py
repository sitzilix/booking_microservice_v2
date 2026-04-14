import asyncio
import json
from aiokafka import AIOKafkaConsumer
from app.core.logger import get_logger

logger = get_logger("NOTIFICATION-SERVICE")

async def consume():
    consumer = AIOKafkaConsumer(
        "booking_created",
        bootstrap_servers='kafka:9092',
        group_id="notification-group",
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    await consumer.start()
    logger.info("Notification Service запущен и слушает топик 'booking_created'...")
    
    try:
        async for msg in consumer:
            event_data = msg.value
            user_id = event_data.get("user_id")
            book_title = event_data.get("book_title")
            
            logger.info(f"ОТПРАВКА EMAIL: Пользователь {user_id}, "
                        f"ваша бронь кинги '{book_title}' подтверждена!")
    except Exception as e:
        logger.error(f"Ошибка при чтении из Kafka: {e}")
    finally:
        await consumer.stop()
        
if __name__ == "__main__":
    asyncio.run(consume())