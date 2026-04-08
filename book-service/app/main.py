from fastapi import FastAPI

app = FastAPI(title="Library API")

@app.get("/")
def home():
    return {"message": "Добро пожаловать в библиотеку!"}