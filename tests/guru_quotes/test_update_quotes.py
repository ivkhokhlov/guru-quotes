from http import HTTPStatus
from httpx import Client
from app.models.Quote import QuoteRead


def test_patch_quote_succeeds(
    api_client: Client,
    created_guru: dict,
    created_quote: dict,
    quote_payload_factory,
) -> None:
    """
    Проверяет успешное обновление текста цитаты.
    """
    guru_id = created_guru["id"]
    quote_id = created_quote["id"]
    update_payload = quote_payload_factory()

    response = api_client.patch(
        f"/api/gurus/{guru_id}/quotes/{quote_id}", json=update_payload
    )
    response_json = response.json()

    assert response.status_code == HTTPStatus.OK
    QuoteRead.model_validate(response_json)
    assert response_json["id"] == quote_id
    assert response_json["text"] == update_payload["text"]
    assert (
        response_json["text"] != created_quote["text"]
    )  # Убедимся, что текст изменился


def test_patch_quote_with_empty_payload_does_not_change_data(
    api_client: Client,
    created_guru: dict,
    created_quote: dict,
) -> None:
    """
    Проверяет, что отправка пустого JSON не изменяет данные цитаты.
    """
    guru_id = created_guru["id"]
    quote_id = created_quote["id"]

    response = api_client.patch(f"/api/gurus/{guru_id}/quotes/{quote_id}", json={})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == created_quote


def test_patch_nonexistent_quote_returns_404(
    api_client: Client,
    created_guru: dict,
    quote_payload_factory,
) -> None:
    """
    Проверяет, что API возвращает 404 при попытке обновить несуществующую цитату.
    """
    guru_id = created_guru["id"]
    non_existent_quote_id = 999999
    payload = quote_payload_factory()

    response = api_client.patch(
        f"/api/gurus/{guru_id}/quotes/{non_existent_quote_id}", json=payload
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
