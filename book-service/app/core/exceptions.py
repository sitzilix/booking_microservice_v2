from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from app.core.logger import get_logger

logger = get_logger("API_EXCEPTION")

class BusinessLogicError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

def setup_exception_handlers(app: FastAPI):
    
    @app.exception_handler(BusinessLogicError)
    async def business_error_handler(request: Request, exc: BusinessLogicError):
        logger.warning(f"Бизнес-отказ: {exc.message}")
        
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
    
    @app.exception_handler(SQLAlchemyError)
    async def db_error_handler(request: Request, exc: SQLAlchemyError):
        logger.error(f"Сбой БД: {str(exc)}")

        return JSONResponse(
            status_code=500,
            content={"detail": "Ошибка базы данных. Проверьте соединение или миграции."}
        )
    @app.exception_handler(Exception)
    async def global_error_handler(request: Request, exc: Exception):
        logger.critical(f"Критическая ошибка: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Внутренняя ошибка сервера."}
        )