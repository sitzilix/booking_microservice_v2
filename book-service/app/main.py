from fastapi import FastAPI
from app.api.authors import router as author_router
from app.api.genres import router as genre_router
from app.api.books import router as book_router

app = FastAPI(title="Library API")

app.include_router(author_router)
app.include_router(genre_router)
app.include_router(book_router)

@app.get("/")
def home():
    return {"message": "Добро пожаловать в библиотеку!"}