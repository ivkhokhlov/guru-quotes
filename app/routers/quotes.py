# app/routers/quotes.py

from http import HTTPStatus
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db.engine import engine
from app.models.Guru import Guru
from app.models.Quote import Quote, QuoteRead


def get_session():
    with Session(engine) as session:
        yield session


router = APIRouter(prefix="/{guru_id}/quotes", tags=["Quotes"])


@router.get("/", summary="Получить все цитаты гуру", response_model=List[QuoteRead])
def get_quotes_by_guru(guru_id: int, session: Session = Depends(get_session)):
    """
    Возвращает список всех цитат для конкретного гуру по его `id`.
    Если гуру не найден, возвращает ошибку 404.
    """
    guru = session.get(Guru, guru_id)
    if not guru:
        raise HTTPException(status_code=404, detail=f"Гуру с ID {guru_id} не найден.")

    return guru.quotes


@router.get(
    "/{quote_id}", summary="Получить конкретную цитату гуру", response_model=QuoteRead
)
def get_specific_quote(
    guru_id: int, quote_id: int, session: Session = Depends(get_session)
):
    """
    Возвращает одну конкретную цитату по `id` гуру и `id` цитаты.
    Если гуру или цитата не найдены, возвращает ошибку 404.
    """
    statement = (
        select(Quote).where(Quote.guru_id == guru_id).where(Quote.id == quote_id)
    )
    quote = session.exec(statement).first()

    if not quote:
        guru = session.get(Guru, guru_id)
        if not guru:
            raise HTTPException(
                status_code=404, detail=f"Гуру с ID {guru_id} не найден."
            )
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Цитата с ID {quote_id} у гуру '{guru.name}' не найдена.",
            )

    return quote
