from httpx import Client
import pytest


@pytest.fixture(scope="session")
def guru_ids_for_cleanup(api_client: Client):
    guru_ids = []
    yield guru_ids

    for guru_id in guru_ids:
        api_client.delete(f"/api/gurus/{guru_id}")


@pytest.fixture(scope="function")
def guru_payload_factory(faker):
    def factory(**args):
        return {
            "name": faker.name(),
            "email": faker.email(),
            "url": faker.url(),
            **args,
        }

    return factory


@pytest.fixture(scope="function")
def created_guru(api_client, guru_payload_factory):
    response = api_client.post("/api/gurus/", json=guru_payload_factory())
    yield response.json()

    api_client.delete(f"/api/gurus/{response.json().get('id')}")
