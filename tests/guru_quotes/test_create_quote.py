from http import HTTPStatus
from httpx import Client
import pytest
from app.models.Quote import QuoteCreate, QuoteRead
from tests.utils.model import get_model_required_fields


def test_create_quote_for_guru_succeeds(
    api_client: Client,
    created_guru: dict,
    quote_payload_factory,
) -> None:
    """
    Проверяет успешное создание цитаты для существующего гуру.
    """
    guru_id = created_guru["id"]
    payload = quote_payload_factory()

    response = api_client.post(f"/api/gurus/{guru_id}/quotes/", json=payload)
    response_json = response.json()

    assert response.status_code == HTTPStatus.CREATED
    QuoteRead.model_validate(response_json)
    assert response_json["text"] == payload["text"]
    assert response_json["guru_id"] == guru_id

    # Очистка
    api_client.delete(f"/api/gurus/{guru_id}/quotes/{response_json['id']}")


def test_create_quote_for_nonexistent_guru_returns_404(
    api_client: Client, quote_payload_factory
) -> None:
    """
    Проверяет, что API возвращает 404 при попытке создать цитату для несуществующего гуру.
    """
    non_existent_guru_id = 999999
    payload = quote_payload_factory()

    response = api_client.post(
        f"/api/gurus/{non_existent_guru_id}/quotes/", json=payload
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    "required_field",
    get_model_required_fields(QuoteCreate),
)
def test_create_quote_without_required_fields_returns_422(
    api_client: Client, created_guru: dict, quote_payload_factory, required_field: str
) -> None:
    """
    Проверяет, что API возвращает 422, если в теле запроса отсутствуют обязательные поля.
    """
    guru_id = created_guru["id"]
    payload = quote_payload_factory()
    del payload[required_field]

    response = api_client.post(f"/api/gurus/{guru_id}/quotes/", json=payload)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
