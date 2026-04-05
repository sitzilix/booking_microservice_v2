from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from .config import settings

# URL должен быть вида: postgresql+asyncpg://user:pass@localhost/dbname
engine = create_async_engine(settings.database_url, echo=True)

# Асинхронная фабрика сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Новый стиль объявления Base (SQLAlchemy 2.0+)
class Base(DeclarativeBase):
    pass

# Асинхронный генератор для FastAPI Dependency Injection
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session