from guru_quotes.data import gurus_db


from fastapi.testclient import TestClient


from http import HTTPStatus


def test_get_quotes_by_guru_success(client: TestClient) -> None:
    """Проверяет успешное получение цитат для существующего гуру."""
    guru_id = 1
    response = client.get(f"/api/gurus/{guru_id}/quotes")
    assert response.status_code == HTTPStatus.OK
    quotes_data = response.json()
    assert isinstance(quotes_data, list)
    original_guru = gurus_db.get(guru_id)
    assert original_guru is not None
    assert len(quotes_data) == len(original_guru.quotes)
    assert quotes_data[0]["text"] == original_guru.quotes[0].text


def test_get_quotes_by_guru_not_found(client: TestClient) -> None:
    """Проверяет получение ошибки 404, если гуру для запроса цитат не найден."""
    guru_id = 999
    response = client.get(f"/api/gurus/{guru_id}/quotes")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": f"Гуру с ID {guru_id} не найден."}
