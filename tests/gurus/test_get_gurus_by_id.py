# === Тесты для эндпоинта /api/gurus/{guru_id} ===


import pytest
from fastapi.testclient import TestClient


from http import HTTPStatus


@pytest.mark.parametrize(
    "guru_id, expected_name, expected_url",
    [
        (
            1,
            "Конфуций",
            "https://ru.wikipedia.org/wiki/%D0%9A%D0%BE%D0%BD%D1%84%D1%83%D1%86%D0%B8%D0%B9",
        ),
        (
            2,
            "Лао-цзы",
            "https://ru.wikipedia.org/wiki/%D0%9B%D0%B0%D0%BE-%D1%86%D0%B7%D1%8B",
        ),
        (3, "QA-Гуру", "https://qa.guru/"),
    ],
)
def test_get_guru_by_id_success(
    client: TestClient, guru_id: int, expected_name: str, expected_url: str
) -> None:
    """Проверяет успешное получение гуру по существующему ID."""
    response = client.get(f"/api/gurus/{guru_id}")
    assert response.status_code == HTTPStatus.OK

    guru_data = response.json()
    assert guru_data["id"] == guru_id
    assert guru_data["name"] == expected_name
    assert "quotes" in guru_data
    assert "url" in guru_data
    assert guru_data["url"] == expected_url


def test_get_guru_by_id_not_found(client: TestClient) -> None:
    """Проверяет получение ошибки 404 для несуществующего ID гуру."""
    guru_id = 999
    response = client.get(f"/api/gurus/{guru_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": f"Гуру с ID {guru_id} не найден."}


def test_get_guru_by_id_invalid_id(client: TestClient) -> None:
    """Проверяет получение ошибки 422 для невалидного ID (не число)."""
    response = client.get("/api/gurus/invalid_id")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
