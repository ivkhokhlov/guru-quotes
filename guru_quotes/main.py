# guru_quotes/main.py

from typing import List

from fastapi import FastAPI, HTTPException

from .data import GURUS_DATA
from .models import Guru, Quote

app = FastAPI(
    title="Guru Quotes API",
    description="Микросервис для получения мудрых цитат от различных гуру.",
    version="1.0.0",
)

# Создадим словари для быстрого доступа по ID, эмулируя работу базы данных
gurus_db = {guru.id: guru for guru in GURUS_DATA}


@app.get(
    "/",
    summary="Корневой эндпоинт",
    description="Простой эндпоинт для проверки работы сервиса.",
)
def read_root():
    return {"message": "Добро пожаловать в Guru Quotes API!"}


@app.get("/api/gurus", response_model=List[Guru], summary="Получить список всех гуру")
def get_all_gurus():
    """
    Возвращает полный список всех гуру и их цитат.
    """
    return list(gurus_db.values())


@app.get(
    "/api/gurus/{guru_id}",
    response_model=Guru,
    summary="Получить конкретного гуру по ID",
)
def get_guru_by_id(guru_id: int):
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
    response_model=List[Quote],
    summary="Получить все цитаты гуру",
)
def get_quotes_by_guru(guru_id: int):
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
    response_model=Quote,
    summary="Получить конкретную цитату гуру",
)
def get_specific_quote(guru_id: int, quote_id: int):
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
