# from http import HTTPStatus
# from fastapi import APIRouter, HTTPException
# from typing import List

# from app.models.Quote import Quote
# from guru_quotes.data import gurus_db

# router = APIRouter(
#     prefix="/api/gurus",
#     tags=["Quotes"]
# )


# @router.get(
#     "/{guru_id}/quotes",
#     summary="Получить все цитаты гуру",
#     status_code=HTTPStatus.OK,
#     response_model=List[Quote]
# )
# def get_quotes_by_guru(guru_id: int) -> List[Quote]:
#     """
#     Возвращает список всех цитат для конкретного гуру по его `id`.
#     Если гуру не найден, возвращает ошибку 404.
#     """
#     guru = gurus_db.get(guru_id)
#     if not guru:
#         raise HTTPException(status_code=404, detail=f"Гуру с ID {guru_id} не найден.")
#     return guru.quotes


# @router.get(
#     "/{guru_id}/quotes/{quote_id}",
#     summary="Получить конкретную цитату гуру",
#     status_code=HTTPStatus.OK,
#     response_model=Quote
# )
# def get_specific_quote(guru_id: int, quote_id: int) -> Quote:
#     """
#     Возвращает одну конкретную цитату по `id` гуру и `id` цитаты.
#     Если гуру или цитата не найдены, возвращает ошибку 404.
#     """
#     guru = gurus_db.get(guru_id)
#     if not guru:
#         raise HTTPException(status_code=404, detail=f"Гуру с ID {guru_id} не найден.")

#     quote = next((q for q in guru.quotes if q.id == quote_id), None)

#     if not quote:
#         raise HTTPException(
#             status_code=404,
#             detail=f"Цитата с ID {quote_id} у гуру {guru.name} не найдена.",
#         )

#     return quote
