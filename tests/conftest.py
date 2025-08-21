import pytest
from fastapi.testclient import TestClient

from guru_quotes.main import app


@pytest.fixture(scope="session")
def client():
    """
    Фикстура, которая создает клиент для тестирования API.
    Использует TestClient, который не требует запущенного сервера.
    """
    with TestClient(app) as test_client:
        yield test_client
