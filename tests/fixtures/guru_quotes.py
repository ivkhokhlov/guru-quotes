import pytest
from httpx import Client


@pytest.fixture(scope="function")
def quote_payload_factory(faker):
    """
    Фабрика для создания данных цитаты.
    """

    def factory(**kwargs):
        payload = {"text": faker.sentence(nb_words=10)}
        payload.update(kwargs)
        return payload

    return factory


@pytest.fixture(scope="function")
def created_quote(api_client: Client, created_guru: dict, quote_payload_factory):
    """
    Создает гуру и цитату для этого гуру.
    После теста удаляет созданную цитату (гуру удаляется своей фикстурой).
    """
    guru_id = created_guru["id"]
    payload = quote_payload_factory()

    response = api_client.post(f"/api/gurus/{guru_id}/quotes/", json=payload)

    assert response.status_code == 201
    quote_data = response.json()

    yield quote_data

    api_client.delete(f"/api/gurus/{guru_id}/quotes/{quote_data['id']}")
