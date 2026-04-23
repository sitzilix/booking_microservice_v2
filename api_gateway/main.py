from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx

from api_gateway import router

app = FastAPI(title="API Gateway")

AUTH_SERVICE_URL = "http://auth_service:8001"
BOOK_SERVICE_URL = "http://book-service:8000"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)