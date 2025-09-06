import pytest
from fastapi.testclient import TestClient

from app.main import app
from httpx import Client
from dotenv import load_dotenv
import os


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope="session")
def client():
    """
    Фикстура, которая создает клиент для тестирования API.
    Использует TestClient, который не требует запущенного сервера.
    """
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session")
def api_client():
    base_url = os.getenv("API_URL", "http://localhost:8000")
    return Client(base_url=base_url)
