from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    # Настройки базы данных
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    JWT_SECRET_KEY: str 
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int 

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Настройки Kafka
    # По умолчанию ставим имя сервиса из docker-compose, но через .env сможем поменять на localhost
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"

    # Настройки Redis 
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    @property
    def redis_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR,".env"), 
        extra="ignore"
    )

settings = Settings()