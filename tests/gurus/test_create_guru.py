import pytest
from httpx import Client
from http import HTTPStatus
from app.models.Guru import Guru, GuruCreate
from tests.utils.model import get_model_required_fields





def test_create_guru_should_return_created_object(
    api_client: Client,
    guru_payload_factory,
    guru_ids_for_cleanup,
) -> None:
    payload = guru_payload_factory()

    response = api_client.post('/api/gurus/', json=payload)
    response_json = response.json()
    guru_ids_for_cleanup.append(response_json.get('id'))

    assert response.status_code == HTTPStatus.CREATED
    assert response_json['name'] == payload['name']
    assert response_json['email'] == payload['email']
    assert response_json['url'] == payload['url']
    Guru.model_validate(response_json)



@pytest.mark.parametrize(
        'required_field',
        get_model_required_fields(GuruCreate),
)
def test_create_guru_without_required_fields_returns_422(
    api_client: Client,
    guru_payload_factory,
    required_field,
) -> None:
    payload = guru_payload_factory()
    del payload[required_field]

    response = api_client.post('/api/gurus/', json=payload)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    'invalid_email',
    [
        'plainaddress',
        '#@%^%#$@#$@#.com',
        '@domain.com',
        'email.domain.com',
        'email@domain@domain.com',
        'email@',
        '',
        '.email@domain.com',
        'email.@domain.com',
        'email..email@domain.com',
        'email withspace@domain.com',
        'email@.domain.com',
        'email@-domain.com',
        'email@domain-.com',
        'email@domain..com',
        'email@123.123.123.123',
        'email@[123.123.123.123]',
        'email@domain.com (Joe Smith)',
        'just"not"right@example.com',
        'this\\ is"not\\allowed@example.com'
    ]
)
def test_create_guru_with_invalid_email_returns_422(
    api_client: Client,
    guru_payload_factory,
    invalid_email,
) -> None:
    payload = guru_payload_factory(email=invalid_email)

    response = api_client.post('/api/gurus/', json=payload)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
