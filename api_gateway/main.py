from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import httpx


from api_gateway.router import router as api_router

@asynccontextmanager
async def lifespan(app: FastAPI):

    app.state.http_client = httpx.AsyncClient(timeout=60.0)
    print("🚀 API Gateway запущен, HTTP клиент готов к работе", flush=True)
    yield

    await app.state.http_client.aclose()
    print("🛑 API Gateway остановлен, клиент закрыт", flush=True)

app = FastAPI(title="API Gateway", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")