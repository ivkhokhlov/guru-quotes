from http import HTTPStatus
from typing import Iterable
from fastapi import APIRouter, HTTPException, Response
from fastapi_pagination import Page, paginate
from sqlmodel import Sequence

from app.db import gurus
from app.models.Guru import Guru, GuruUpdate


router = APIRouter(
    prefix="/api/gurus",
    tags=["Gurus"],
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
    status_code=HTTPStatus.CREATED,
)
def create_guru(guru: Guru) -> Guru:
    return gurus.create_guru(guru)



@router.delete(
    "/{guru_id}",
    summary="Удалить гуру по ID",
    status_code=HTTPStatus.NO_CONTENT,
)
def delete_guru(guru_id: int) -> Response:
    """
    Удаляет одного гуру по его уникальному `id`.
    Если гуру не найден, возвращает ошибку 404.
    В случае успеха возвращает ответ 204 No Content.
    """
    deleted_guru = gurus.delete_guru(guru_id)
    if not deleted_guru:
        raise HTTPException(status_code=404, detail=f"Гуру с ID {guru_id} не найден.")

    return Response(status_code=HTTPStatus.NO_CONTENT)


@router.patch(
    "/{guru_id}",
    summary="Обновить данные гуру по ID",
    status_code=HTTPStatus.OK,
)
def patch_guru(guru_id: int, guru_data: GuruUpdate) -> Guru:
    """
    Частично обновляет данные гуру по его уникальному `id`.
    Можно передать любое количество полей для обновления: `name`, `email`, `url`.
    Если гуру не найден, возвращает ошибку 404.
    """
    updated_guru = gurus.patch_guru(guru_id, guru_data)
    if not updated_guru:
        raise HTTPException(status_code=404, detail=f"Гуру с ID {guru_id} не найден.")

    return updated_guru
