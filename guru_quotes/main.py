from http import HTTPStatus
import json
from fastapi import FastAPI, HTTPException
from guru_quotes.data import gurus_db
from fastapi_pagination import Page, add_pagination, paginate

from guru_quotes.models import Guru, Quote

app = FastAPI(
    title="Guru Quotes API",
    description="Микросервис для получения мудрых цитат от различных гуру.",
    version="0.2.0",
)
add_pagination(app)


@app.get(
    "/",
    summary="Корневой эндпоинт",
    description="Простой эндпоинт для проверки работы сервиса.",
    status_code=HTTPStatus.OK,
)
def read_root():
    return {
        "message": "Добро пожаловать в Guru Quotes API!",
        "gurus_count": len(gurus_db),
    }


@app.get(
    "/api/gurus",
    summary="Получить список всех гуру",
    status_code=HTTPStatus.OK,
)
def get_all_gurus() -> Page[Guru]:
    """
    Возвращает полный список всех гуру и их цитат.
    """
    return paginate((list(gurus_db.values())))


@app.get(
    "/api/gurus/{guru_id}",
    summary="Получить конкретного гуру по ID",
    status_code=HTTPStatus.OK,
)
def get_guru_by_id(guru_id: int) -> Guru:
    """
    Возвращает одного гуру по его уникальному `id`.
    Если гуру не найден, возвращает ошибку 404.
    """
    guru = gurus_db.get(guru_id)
    if not guru:
        raise HTTPException(status_code=404, detail=f"Гуру с ID {guru_id} не найден.")
    return guru


@app.get(
    "/api/gurus/{guru_id}/quotes",
    summary="Получить все цитаты гуру",
    status_code=HTTPStatus.OK,
)
def get_quotes_by_guru(guru_id: int) -> list[Quote]:
    """
    Возвращает список всех цитат для конкретного гуру по его `id`.
    Если гуру не найден, возвращает ошибку 404.
    """
    guru = gurus_db.get(guru_id)
    if not guru:
        raise HTTPException(status_code=404, detail=f"Гуру с ID {guru_id} не найден.")
    return guru.quotes


@app.get(
    "/api/gurus/{guru_id}/quotes/{quote_id}",
    summary="Получить конкретную цитату гуру",
    status_code=HTTPStatus.OK,
)
def get_specific_quote(guru_id: int, quote_id: int) -> Quote:
    """
    Возвращает одну конкретную цитату по `id` гуру и `id` цитаты.
    Если гуру или цитата не найдены, возвращает ошибку 404.
    """
    guru = gurus_db.get(guru_id)
    if not guru:
        raise HTTPException(status_code=404, detail=f"Гуру с ID {guru_id} не найден.")

    quote = next((q for q in guru.quotes if q.id == quote_id), None)

    if not quote:
        raise HTTPException(
            status_code=404,
            detail=f"Цитата с ID {quote_id} у гуру {guru.name} не найдена.",
        )

    return quote
