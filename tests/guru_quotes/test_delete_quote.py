from http import HTTPStatus
from httpx import Client


def test_delete_quote_succeeds(
    api_client: Client, created_guru: dict, quote_payload_factory
) -> None:
    """
    Проверяет успешное удаление цитаты.
    Фикстура 'created_quote' здесь не используется, чтобы избежать двойного удаления.
    """
    guru_id = created_guru["id"]

    create_response = api_client.post(
        f"/api/gurus/{guru_id}/quotes/", json=quote_payload_factory()
    )
    assert create_response.status_code == HTTPStatus.CREATED
    quote_id = create_response.json()["id"]

    delete_response = api_client.delete(f"/api/gurus/{guru_id}/quotes/{quote_id}")
    assert delete_response.status_code == HTTPStatus.NO_CONTENT

    get_response = api_client.get(f"/api/gurus/{guru_id}/quotes/{quote_id}")
    assert get_response.status_code == HTTPStatus.NOT_FOUND


def test_delete_nonexistent_quote_returns_404(
    api_client: Client, created_guru: dict
) -> None:
    """
    Проверяет, что API возвращает 404 при попытке удалить несуществующую цитату.
    """
    guru_id = created_guru["id"]
    non_existent_quote_id = 999999

    response = api_client.delete(f"/api/gurus/{guru_id}/quotes/{non_existent_quote_id}")

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_quote_from_nonexistent_guru_returns_404(api_client: Client) -> None:
    """
    Проверяет, что API возвращает 404 при попытке удалить цитату у несуществующего гуру.
    """
    non_existent_guru_id = 999999

    response = api_client.delete(f"/api/gurus/{non_existent_guru_id}/quotes/1")

    assert response.status_code == HTTPStatus.NOT_FOUND
