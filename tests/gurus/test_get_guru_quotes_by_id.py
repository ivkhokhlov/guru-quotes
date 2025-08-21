import pytest
from fastapi.testclient import TestClient


from http import HTTPStatus

from guru_quotes.data import gurus_db


@pytest.mark.parametrize(
    "guru_id, quote_id, expected_text_part",
    [
        (1, 1, "Не тот велик"),
        (2, 2, "Знающий не говорит"),
        (3, 3, "Не захардкодь"),
    ],
)
def test_get_specific_quote_success(
    client: TestClient, guru_id: int, quote_id: int, expected_text_part: str
) -> None:
    """Проверяет успешное получение конкретной цитаты."""
    response = client.get(f"/api/gurus/{guru_id}/quotes/{quote_id}")
    assert response.status_code == HTTPStatus.OK
    quote_data = response.json()
    assert quote_data["id"] == quote_id
    assert expected_text_part in quote_data["text"]


def test_get_specific_quote_guru_not_found(client: TestClient) -> None:
    """Проверяет ошибку 404, если гуру для цитаты не найден."""
    guru_id = 999
    quote_id = 1
    response = client.get(f"/api/gurus/{guru_id}/quotes/{quote_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": f"Гуру с ID {guru_id} не найден."}


def test_get_specific_quote_not_found(client: TestClient) -> None:
    """Проверяет ошибку 404, если сама цитата у существующего гуру не найдена."""
    guru_id = 1
    quote_id = 999
    response = client.get(f"/api/gurus/{guru_id}/quotes/{quote_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND
    guru_name = gurus_db[guru_id].name
    assert response.json() == {
        "detail": f"Цитата с ID {quote_id} у гуру {guru_name} не найдена."
    }


def test_get_specific_quote_invalid_ids(client: TestClient) -> None:
    """Проверяет ошибку 422 для невалидных ID гуру или цитаты."""
    response = client.get("/api/gurus/invalid/quotes/1")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    response = client.get("/api/gurus/1/quotes/invalid")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
