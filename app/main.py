from dotenv import load_dotenv

load_dotenv()

from contextlib import asynccontextmanager
from app.db.engine import create_db_and_tables
from app.db.seeding import seed_database
from http import HTTPStatus
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.routers import gurus, quotes, status


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    print("INFO:     Application startup...")
    create_db_and_tables()
    seed_database()
    print("INFO:     Database tables created (if not exist).")
    yield
    print("INFO:     Application shutdown...")


app = FastAPI(
    title="Guru Quotes API",
    description="Микросервис для получения мудрых цитат от различных гуру.",
    version="0.2.0",
    lifespan=lifespan,
)

app.include_router(gurus.router)
app.include_router(quotes.router, prefix="/api/gurus")
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
