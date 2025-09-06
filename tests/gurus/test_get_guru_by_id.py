import pytest
from httpx import Client
from http import HTTPStatus
from app.models.Guru import Guru


def test_created_guru_should_be_found_by_id(
    api_client: Client,
    created_guru,
) -> None:
    guru_id = created_guru.get('id')
    response = api_client.get(f'/api/gurus/{guru_id}')
    response_json = response.json()

    assert response.status_code == HTTPStatus.OK
    Guru.model_validate(response_json)
    assert response_json['name'] == created_guru['name']
    assert response_json['email'] == created_guru['email']
    assert response_json['url'] == created_guru['url']


def test_get_guru_by_id_from_list_returns_same_values(
    api_client: Client,
    created_guru,
) -> None:
    response_from_list = api_client.get(f'/api/gurus/')
    if not response_from_list.json().get('items'):
        pytest.skip('Gurus list is empty')

    response_by_id = api_client.get(f'/api/gurus/{response_from_list.json().get("items")[0].get("id")}')

    assert response_by_id.json() == response_from_list.json().get('items')[0]


def test_get_guru_by_id_with_invalid_id_returns_404(
    api_client: Client,
) -> None:
    response = api_client.get(f'/api/gurus/444444444')

    assert response.status_code == HTTPStatus.NOT_FOUND
