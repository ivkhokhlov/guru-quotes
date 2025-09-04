from http import HTTPStatus
from typing import Iterable
from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page, paginate
from sqlmodel import Sequence

from app.db import gurus
from app.models.Guru import Guru


router = APIRouter(
    prefix="/api/gurus",
    tags=["Gurus"]
)


@router.get(
    "/",
    summary="Получить список всех гуру",
    status_code=HTTPStatus.OK,
)
def get_all_gurus() -> Page[Guru]:
    """
    Возвращает полный список всех гуру и их цитат.
    """
    return paginate(gurus.get_all_gurus())


@router.get(
    "/{guru_id}",
    summary="Получить конкретного гуру по ID",
    status_code=HTTPStatus.OK,
)
def get_guru_by_id(guru_id: int) -> Guru:
    """
    Возвращает одного гуру по его уникальному `id`.
    Если гуру не найден, возвращает ошибку 404.
    """
    guru = gurus.get_guru_by_id(guru_id)
    if not guru:
        raise HTTPException(status_code=404, detail=f"Гуру с ID {guru_id} не найден.")

    return guru


@router.post(
    "/",
    summary="Получить конкретного гуру по ID",
    status_code=HTTPStatus.OK,
)
def create_guru(guru: Guru) -> Guru:
    """
    Возвращает одного гуру по его уникальному `id`.
    Если гуру не найден, возвращает ошибку 404.
    """
    return gurus.create_guru(guru)
