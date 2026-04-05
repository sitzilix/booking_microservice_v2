from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Настройки базы данных
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    # Склеиваем URL для SQLAlchemy (тот самый asyncpg, о котором говорили)
    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Настройки Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"

    # Загрузка переменных из файла .env
    model_config = SettingsConfigDict(env_file=".env")

# Создаем экземпляр, который будем импортировать в другие файлы
settings = Settings()