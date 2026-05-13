import httpx
from fastapi import FastAPI, APIRouter, Request, HTTPException, Depends
from fastapi.responses import StreamingResponse
from starlette.background import BackgroundTask
from contextlib import asynccontextmanager
from common.dependencies import get_current_user_id 

HOP_BY_HOP_HEADERS = {
    "connection", "keep-alive", "proxy-authenticate", 
    "proxy-authorization", "te", "trailers", 
    "transfer-encoding", "upgrade", "host"
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx.AsyncClient(
        timeout=60.0,
        limits=httpx.Limits(max_connections=100, max_keepalive_connections=20)
    )
    print("🚀 API Gateway запущен, HTTP клиент инициализирован")
    yield
    await app.state.http_client.aclose()
    print("🛑 API Gateway остановлен, соединения закрыты")

app = FastAPI(lifespan=lifespan)
router = APIRouter()

AUTH_SERVICE_URL = "http://auth_service:8000"
BOOK_SERVICE_URL = "http://book-service:8000"

async def forward_request(target_url: str, request: Request, extra_headers: dict = None):

    client: httpx.AsyncClient = request.app.state.http_client

    headers = {
        k: v for k, v in request.headers.items() 
        if k.lower() not in HOP_BY_HOP_HEADERS
    }
    

    if extra_headers:
        headers.update(extra_headers)

 
    headers["X-Forwarded-For"] = request.client.host

    try:
        # Формируем запрос к микросервису
        rp_req = client.build_request(
            method=request.method,
            url=target_url,
            content=request.stream(),
            params=request.query_params,
            headers=headers
        )


        response = await client.send(rp_req, stream=True)

        response_headers = {
            k: v for k, v in response.headers.items() 
            if k.lower() not in HOP_BY_HOP_HEADERS
        }

        return StreamingResponse(
            response.aiter_raw(),
            status_code=response.status_code,
            headers=response_headers,
            background=BackgroundTask(response.aclose)
        )

    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail=f"Сервис временно недоступен: {exc}")


@router.api_route("/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_auth(path: str, request: Request):
    target_url = f"{AUTH_SERVICE_URL}/{path.lstrip('/')}"
    return await forward_request(target_url, request)

@router.api_route("/books/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_books(
    path: str, 
    request: Request, 
    user_id: int = Depends(get_current_user_id) 
):
    target_url = f"{BOOK_SERVICE_URL}/{path.lstrip('/')}"
    custom_headers = {"X-User-Id": str(user_id)}
    return await forward_request(target_url, request, custom_headers)

app.include_router(router)