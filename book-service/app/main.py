from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.authors import router as author_router
from app.api.genres import router as genre_router
from app.api.books import router as book_router

from app.api.bookings import router as booking_router
from app.core.kafka import kafka_manager

from app.core.exceptions import setup_exception_handlers

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Запуск сервиса: Подключение к Kafka...")
    await kafka_manager.start()
    
    yield 
    
    print("🛑 Остановка сервиса: Закрытие соединений...")
    await kafka_manager.stop()

app = FastAPI(
    title="Library API (Book Service)",
    lifespan=lifespan
)

setup_exception_handlers(app)

# Подключаем роуты
app.include_router(author_router)
app.include_router(genre_router)
app.include_router(book_router)
app.include_router(booking_router) # Регистрация нового роута

@app.get("/")
def home():
    return {"message": "Добро пожаловать в библиотеку!"}