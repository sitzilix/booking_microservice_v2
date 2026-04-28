import redis.asyncio as redis
from common.config import settings

redis_client = redis.from_url(
    settings.redis_url,
    decode_responses=True,
    encoding="utf-8"
)

async def init_redis():
    try:
        await redis_client.ping()
        print("✅ Успешное подключение к Redis")
    except Exception as e:
        print(f"❌ Ошибка подключения к Redis: {e}")