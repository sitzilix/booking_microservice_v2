import asyncio
import json
import logging
from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaConnectionError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KafkaManager:
    def __init__(self):
        self.producer = None

    async def start(self):
        """Запуск продюсера с бесконечными попытками подключения"""
        logger.info("🚀 Запуск сервиса: Подключение к Kafka...")
        
        while True:
            try:
                self.producer = AIOKafkaProducer(
                    bootstrap_servers='kafka:9092',
                    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                    # Исправленные названия параметров:
                    request_timeout_ms=5000,
                    retry_backoff_ms=1000 
                )
                await self.producer.start()
                logger.info("✅ Успешное подключение к Kafka!")
                break  # Выходим из цикла, если подключились
            except (KafkaConnectionError, ConnectionRefusedError) as e:
                logger.error(f"⏳ Kafka пока недоступна ({e}). Повтор через 5 секунд...")
                await asyncio.sleep(5)
            except Exception as e:
                logger.error(f"❌ Критическая ошибка при старте Kafka: {e}")
                # Если ошибка не связана с сетью, лучше подождать чуть дольше
                await asyncio.sleep(10)

    async def stop(self):
        """Остановка продюсера"""
        if self.producer:
            await self.producer.stop()
            logger.info("🛑 Соединение с Kafka закрыто")

    async def send_event(self, topic: str, data: dict):
        """Метод для отправки сообщения"""
        if self.producer:
            try:
                await self.producer.send_and_wait(topic, data)
                logger.info(f"📨 Сообщение отправлено в топик {topic}")
            except Exception as e:
                logger.error(f"⚠️ Не удалось отправить сообщение в Kafka: {e}")
        else:
            logger.warning("🚫 Продюсер Kafka не инициализирован!")

kafka_manager = KafkaManager()