from http import HTTPStatus

import pytest
from httpx import Client

from app.models.Guru import Guru, GuruUpdate
from tests.utils.model import get_model_fields, get_model_required_fields


def test_patch_guru_all_fields_should_succeed(
    api_client: Client,
    created_guru: dict,
    guru_payload_factory,
) -> None:
    """
    Проверяет успешное обновление всех полей гуру одним запросом.
    """
    guru_id = created_guru.get("id")
    update_payload = guru_payload_factory()

    response = api_client.patch(f"/api/gurus/{guru_id}", json=update_payload)
    response_json = response.json()

    get_response = api_client.get(f"/api/gurus/{guru_id}")

    assert response.status_code == HTTPStatus.OK
    Guru.model_validate(response_json)
    assert response_json["name"] == update_payload["name"]
    assert response_json["email"] == update_payload["email"]
    assert response_json["url"] == update_payload["url"]

    assert get_response.json() == response_json


@pytest.mark.parametrize(
    'field_to_update',
    get_model_fields(GuruUpdate),
)
def test_patch_guru_single_field_should_succeed(
    api_client: Client,
    created_guru: dict,
    field_to_update: str,
    guru_payload_factory,
) -> None:
    """
    Проверяет успешное частичное обновление одного поля гуру.
    """
    guru_id = created_guru.get('id')
    new_value = guru_payload_factory()[field_to_update]

    response = api_client.patch(f"/api/gurus/{guru_id}", json={field_to_update: new_value})
    response_json = response.json()

    assert response.status_code == HTTPStatus.OK
    Guru.model_validate(response_json)

    assert response_json[field_to_update] == new_value

    for key, value in created_guru.items():
        if key != field_to_update and key in response_json:
            assert response_json[key] == value


def test_patch_guru_with_empty_payload_should_not_change_data(
    api_client: Client,
    created_guru: dict,
) -> None:
    """
    Проверяет, что отправка пустого payload не изменяет данные гуру.
    """
    guru_id = created_guru.get("id")
    update_payload = {}

    response = api_client.patch(f"/api/gurus/{guru_id}", json=update_payload)
    response_json = response.json()

    assert response.status_code == HTTPStatus.OK
    # Ответ должен полностью совпадать с исходным объектом
    assert response_json == created_guru


def test_patch_guru_with_nonexistent_id_should_return_404(
    api_client: Client,
    guru_payload_factory,
) -> None:
    """
    Проверяет, что API возвращает 404 при попытке обновить несуществующего гуру.
    """
    non_existent_id = 9999999
    update_payload = guru_payload_factory()

    response = api_client.patch(f"/api/gurus/{non_existent_id}", json=update_payload)

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_patch_guru_with_invalid_email_should_return_422(
    api_client: Client,
    created_guru: dict,
) -> None:
    """
    Проверяет, что API возвращает 422 при попытке обновить email на невалидное значение.
    """
    guru_id = created_guru.get("id")
    update_payload = {"email": "not-a-valid-email"}

    response = api_client.patch(f"/api/gurus/{guru_id}", json=update_payload)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
