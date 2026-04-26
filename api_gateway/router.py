from fastapi import APIRouter, Request, Response, Depends, HTTPException
import httpx

from common.dependencies import get_current_user_id 

router = APIRouter()

AUTH_SERVICE_URL = "http://auth_service:8000"
BOOK_SERVICE_URL = "http://book-service:8000"

@router.api_route("/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_auth(path: str, request: Request):
    
    clean_path = path.lstrip('/')
    target_url = f"{AUTH_SERVICE_URL}/{clean_path}"

    return await forward_request(target_url, request)

@router.api_route("/books/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_books(
    path: str, 
    request: Request, 
    user_id: int = Depends(get_current_user_id) 
):
    clean_path = path.strip("/")
    target_url = f"{BOOK_SERVICE_URL}/{path}"
    custom_headers = {"X-User-Id": str(user_id)}
    
    return await forward_request(target_url, request, custom_headers)

async def forward_request(target_url: str, request: Request, extra_headers: dict = None):
    content = await request.body()
    query_params = request.query_params
    headers = dict(request.headers)
    headers = dict(request.headers)
    
    headers["X-Forwarded-Host"] = request.headers.get("host", "localhost:8080")
    headers["X-Forwarded-Proto"] = request.url.scheme 
    
    if extra_headers:
        headers.update(extra_headers)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=target_url,
                content=content,
                params=query_params,
                headers=headers,
                timeout=10.0 
            ) 
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Сервис недоступен: {exc}")