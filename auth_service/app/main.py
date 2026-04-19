from fastapi import FastAPI
from app.api.users import router as auth_router

app = FastAPI(title="Auth-service")

app.include_router(auth_router, prefix="/api")

@app.get("/healthcheck")
async def health():
    return {"status": "ok"}