from http import HTTPStatus
from httpx import Client


def test_read_root(api_client: Client) -> None:
    """Проверяет успешный ответ от корневого эндпоинта."""
    response = api_client.get("/")
    response_json = response.json()

    assert response.status_code == HTTPStatus.OK
    assert response_json["message"] == "Добро пожаловать в Guru Quotes API!"


def test_db_is_available(api_client: Client) -> None:
    """Проверяет успешный ответ от корневого эндпоинта."""
    response = api_client.get("status/")
    response_json = response.json()

    assert response.status_code == HTTPStatus.OK
    assert response_json.get("is_db_available") is True
