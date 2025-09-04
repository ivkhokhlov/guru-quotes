from dotenv import load_dotenv
# Add this import
from contextlib import asynccontextmanager

from app.db.engine import create_db_and_tables

load_dotenv()


from http import HTTPStatus
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.routers import gurus, quotes, status


# 1. Define the lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This code runs on startup
    print("INFO:     Application startup...")
    create_db_and_tables()
    print("INFO:     Database tables created (if not exist).")
    yield
    print("INFO:     Application shutdown...")


# 2. Pass the lifespan manager to the FastAPI instance
app = FastAPI(
    title="Guru Quotes API",
    description="Микросервис для получения мудрых цитат от различных гуру.",
    version="0.2.0",
    lifespan=lifespan  # Add this line
)

app.include_router(gurus.router)
# app.include_router(quotes.router)
app.include_router(status.router)

add_pagination(app)


@app.get(
    "/",
    summary="Корневой эндпоинт",
    description="Простой эндпоинт для проверки работы сервиса.",
    status_code=HTTPStatus.OK,
    tags=["Root"],
)
def read_root():
    """
    Возвращает приветственное сообщение.
    """
    return {
        "message": "Добро пожаловать в Guru Quotes API!",
    }
