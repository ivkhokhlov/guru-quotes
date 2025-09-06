from http import HTTPStatus
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session, select

from app.db.engine import engine
from app.models.Guru import Guru
from app.models.Quote import Quote, QuoteCreate, QuoteRead, QuoteUpdate


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


@router.post(
    "/",
    summary="Создать новую цитату для гуру",
    status_code=HTTPStatus.CREATED,
    response_model=QuoteRead,
)
def create_quote_for_guru(
    guru_id: int, quote_data: QuoteCreate, session: Session = Depends(get_session)
):
    """
    Создает новую цитату для указанного гуру.
    Если гуру не найден, возвращает ошибку 404.
    """
    guru = session.get(Guru, guru_id)
    if not guru:
        raise HTTPException(status_code=404, detail=f"Гуру с ID {guru_id} не найден.")

    new_quote = Quote.model_validate(quote_data, update={"guru_id": guru_id})

    session.add(new_quote)
    session.commit()
    session.refresh(new_quote)

    return new_quote


@router.patch(
    "/{quote_id}",
    summary="Обновить цитату гуру",
    response_model=QuoteRead,
)
def update_quote(
    guru_id: int,
    quote_id: int,
    quote_update: QuoteUpdate,
    session: Session = Depends(get_session),
):
    """
    Частично обновляет данные цитаты.
    Если гуру или цитата не найдены, возвращает ошибку 404.
    """
    guru = session.get(Guru, guru_id)
    if not guru:
        raise HTTPException(status_code=404, detail=f"Гуру с ID {guru_id} не найден.")

    statement = (
        select(Quote).where(Quote.guru_id == guru_id).where(Quote.id == quote_id)
    )
    db_quote = session.exec(statement).first()

    if not db_quote:
        raise HTTPException(
            status_code=404,
            detail=f"Цитата с ID {quote_id} у гуру '{guru.name}' не найдена.",
        )

    update_data = quote_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_quote, key, value)

    session.add(db_quote)
    session.commit()
    session.refresh(db_quote)

    return db_quote


@router.delete(
    "/{quote_id}", summary="Удалить цитату гуру", status_code=HTTPStatus.NO_CONTENT
)
def delete_quote(guru_id: int, quote_id: int, session: Session = Depends(get_session)):
    """
    Удаляет цитату по `id` гуру и `id` цитаты.
    Если гуру или цитата не найдены, возвращает ошибку 404.
    """
    guru = session.get(Guru, guru_id)
    if not guru:
        raise HTTPException(status_code=404, detail=f"Гуру с ID {guru_id} не найден.")

    statement = (
        select(Quote).where(Quote.guru_id == guru_id).where(Quote.id == quote_id)
    )
    quote_to_delete = session.exec(statement).first()

    if not quote_to_delete:
        raise HTTPException(
            status_code=404,
            detail=f"Цитата с ID {quote_id} у гуру '{guru.name}' не найдена.",
        )

    session.delete(quote_to_delete)
    session.commit()

    return Response(status_code=HTTPStatus.NO_CONTENT)
