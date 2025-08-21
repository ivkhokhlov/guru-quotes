from http import HTTPStatus

from fastapi.testclient import TestClient

from tests.test_api import TOTAL_GURUS
from guru_quotes.data import GURUS_DATA

TOTAL_GURUS = len(GURUS_DATA)


def test_read_root(client: TestClient) -> None:
    """Проверяет успешный ответ от корневого эндпоинта."""
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert response_json["message"] == "Добро пожаловать в Guru Quotes API!"
    assert response_json["gurus_count"] == TOTAL_GURUS
