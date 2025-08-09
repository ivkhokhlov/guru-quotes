# tests/test_api.py

import pytest
from fastapi.testclient import TestClient

from guru_quotes.data import \
    GURUS_DATA  # Импортируем исходные данные для сравнения

# === Тесты для корневого эндпоинта (/) ===


def test_read_root(client: TestClient) -> None:
    """Проверяет успешный ответ от корневого эндпоинта."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Добро пожаловать в Guru Quotes API!"}


# === Тесты для эндпоинта /api/gurus ===


def test_get_all_gurus(client: TestClient) -> None:
    """Проверяет получение списка всех гуру."""
    response = client.get("/api/gurus")
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)
    # Убедимся, что API возвращает то же количество гуру, что и в "базе данных"
    assert len(response_data) == len(GURUS_DATA)
    # Проверим, что имя первого гуру совпадает для базовой уверенности в данных
    assert response_data[0]["name"] == GURUS_DATA[0].name


# === Тесты для эндпоинта /api/gurus/{guru_id} ===


@pytest.mark.parametrize(
    "guru_id, expected_name",
    [
        (1, "Конфуций"),
        (2, "Лао-цзы"),
        (3, "QA-Гуру"),
    ],
)
def test_get_guru_by_id_success(
    client: TestClient, guru_id: int, expected_name: str
) -> None:
    """Проверяет успешное получение гуру по существующему ID."""
    response = client.get(f"/api/gurus/{guru_id}")
    assert response.status_code == 200

    guru_data = response.json()
    assert guru_data["id"] == guru_id
    assert guru_data["name"] == expected_name
    assert "quotes" in guru_data


def test_get_guru_by_id_not_found(client: TestClient) -> None:
    """Проверяет получение ошибки 404 для несуществующего ID гуру."""
    guru_id = 999
    response = client.get(f"/api/gurus/{guru_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Гуру с ID {guru_id} не найден."}


def test_get_guru_by_id_invalid_id(client: TestClient) -> None:
    """Проверяет получение ошибки 422 для невалидного ID (не число)."""
    response = client.get("/api/gurus/invalid_id")
    # FastAPI автоматически валидирует типы пути и возвращает 422
    assert response.status_code == 422


# === Тесты для эндпоинта /api/gurus/{guru_id}/quotes ===


def test_get_quotes_by_guru_success(client: TestClient) -> None:
    """Проверяет успешное получение цитат для существующего гуру."""
    guru_id = 1
    response = client.get(f"/api/gurus/{guru_id}/quotes")
    assert response.status_code == 200
    quotes_data = response.json()
    assert isinstance(quotes_data, list)
    # Сравним с исходными данными
    original_guru = next((g for g in GURUS_DATA if g.id == guru_id), None)
    assert len(quotes_data) == len(original_guru.quotes)
    assert quotes_data[0]["text"] == original_guru.quotes[0].text


def test_get_quotes_by_guru_not_found(client: TestClient) -> None:
    """Проверяет получение ошибки 404, если гуру для запроса цитат не найден."""
    guru_id = 999
    response = client.get(f"/api/gurus/{guru_id}/quotes")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Гуру с ID {guru_id} не найден."}


# === Тесты для эндпоинта /api/gurus/{guru_id}/quotes/{quote_id} ===


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
    assert response.status_code == 200
    quote_data = response.json()
    assert quote_data["id"] == quote_id
    assert expected_text_part in quote_data["text"]


def test_get_specific_quote_guru_not_found(client: TestClient) -> None:
    """Проверяет ошибку 404, если гуру для цитаты не найден."""
    guru_id = 999
    quote_id = 1
    response = client.get(f"/api/gurus/{guru_id}/quotes/{quote_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Гуру с ID {guru_id} не найден."}


def test_get_specific_quote_not_found(client: TestClient) -> None:
    """Проверяет ошибку 404, если сама цитата у существующего гуру не найдена."""
    guru_id = 1
    quote_id = 999
    response = client.get(f"/api/gurus/{guru_id}/quotes/{quote_id}")
    assert response.status_code == 404
    # Имя гуру берется из "базы данных" для сообщения об ошибке
    guru_name = GURUS_DATA[0].name
    assert response.json() == {
        "detail": f"Цитата с ID {quote_id} у гуру {guru_name} не найдена."
    }


def test_get_specific_quote_invalid_ids(client: TestClient) -> None:
    """Проверяет ошибку 422 для невалидных ID гуру или цитаты."""
    response = client.get("/api/gurus/invalid/quotes/1")
    assert response.status_code == 422
    response = client.get("/api/gurus/1/quotes/invalid")
    assert response.status_code == 422
