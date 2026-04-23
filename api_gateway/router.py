from fastapi import APIRouter, Request, Response, Depends, HTTPException
import httpx
# Импортируем твою функцию проверки токена
from common.dependencies import get_current_user_id 

router = APIRouter()

# Адреса сервисов внутри сети Docker
AUTH_SERVICE_URL = "http://auth-service:8001"
BOOK_SERVICE_URL = "http://book-service:8000"

# 1. МАРШРУТЫ ДЛЯ AUTH (БЕЗ ПРОВЕРКИ ТОКЕНА)
@router.api_route("/api/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_auth(path: str, request: Request):
    """
    Пробрасывает всё, что идет на /api/auth/* прямиком в auth-service.
    Регистрация и логин должны быть доступны всем.
    """
    target_url = f"{AUTH_SERVICE_URL}/{path}"
    return await forward_request(target_url, request)


# 2. МАРШРУТЫ ДЛЯ BOOKS (С ПРОВЕРКОЙ ТОКЕНА)
@router.api_route("/api/books/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_books(
    path: str, 
    request: Request, 
    user_id: int = Depends(get_current_user_id) # Сначала проверяем JWT
):
    """
    Пробрасывает запросы в book-service только если токен валидный.
    Добавляет ID пользователя в заголовки для микросервиса.
    """
    target_url = f"{BOOK_SERVICE_URL}/{path}"
    
    # Добавляем ID пользователя в заголовки, чтобы book-service знал, кто делает запрос
    custom_headers = {"X-User-Id": str(user_id)}
    
    return await forward_request(target_url, request, custom_headers)


# 3. ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ ПРОБРОСА
async def forward_request(target_url: str, request: Request, extra_headers: dict = None):
    """
    Механика пересылки запроса: берет входящий запрос и отправляет его копию в микросервис.
    """
    # 1. Собираем данные из оригинального запроса
    content = await request.body()
    query_params = request.query_params
    headers = dict(request.headers)
    
    # Удаляем заголовок 'host', так как он будет другим для микросервиса
    headers.pop("host", None)
    
    # Добавляем кастомные заголовки (например, X-User-Id)
    if extra_headers:
        headers.update(extra_headers)

    async with httpx.AsyncClient() as client:
        try:
            # 2. Делаем запрос к микросервису
            response = await client.request(
                method=request.method,
                url=target_url,
                content=content,
                params=query_params,
                headers=headers,
                timeout=10.0 # Чтобы не ждать вечно, если сервис упал
            )
            
            # 3. Возвращаем ответ микросервиса клиенту (браузеру)
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Сервис недоступен: {exc}")