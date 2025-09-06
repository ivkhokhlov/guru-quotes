from http import HTTPStatus
from httpx import Client
from app.models.Quote import QuoteRead


def test_get_all_quotes_for_guru_succeeds(
    api_client: Client,
    created_guru: dict,
    created_quote: dict,
) -> None:
    """
    Проверяет успешное получение списка всех цитат для конкретного гуру.
    """
    guru_id = created_guru["id"]

    response = api_client.get(f"/api/gurus/{guru_id}/quotes/")
    response_json = response.json()

    assert response.status_code == HTTPStatus.OK
    assert isinstance(response_json, list)
    assert len(response_json) > 0
    assert created_quote in response_json

    for quote in response_json:
        QuoteRead.model_validate(quote)


def test_get_specific_quote_succeeds(
    api_client: Client,
    created_guru: dict,
    created_quote: dict,
) -> None:
    """
    Проверяет успешное получение одной конкретной цитаты по ID.
    """
    guru_id = created_guru["id"]
    quote_id = created_quote["id"]

    response = api_client.get(f"/api/gurus/{guru_id}/quotes/{quote_id}")
    response_json = response.json()

    assert response.status_code == HTTPStatus.OK
    QuoteRead.model_validate(response_json)
    assert response_json == created_quote


def test_get_quote_for_nonexistent_guru_returns_404(
    api_client: Client,
) -> None:
    """
    Проверяет, что API возвращает 404 при запросе цитаты у несуществующего гуру.
    """
    response = api_client.get("/api/gurus/999999/quotes/1")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_get_nonexistent_quote_returns_404(
    api_client: Client,
    created_guru: dict,
) -> None:
    """
    Проверяет, что API возвращает 404 при запросе несуществующей цитаты.
    """
    guru_id = created_guru["id"]
    non_existent_quote_id = 999999

    response = api_client.get(f"/api/gurus/{guru_id}/quotes/{non_existent_quote_id}")

    assert response.status_code == HTTPStatus.NOT_FOUND
