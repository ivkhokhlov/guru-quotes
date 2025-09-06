from fastapi_pagination import Page
from httpx import Client
from http import HTTPStatus

import pytest
from app.models.Guru import Guru


def test_get_gurus_list_should_not_be_empty(
    api_client: Client,
) -> None:
    response = api_client.get("/api/gurus/")
    response_json = response.json()

    assert response.status_code == HTTPStatus.OK
    assert len(response_json.get("items")) > 0
    Page[Guru].model_validate(response_json)


def test_get_gurus_list_should_have_unique_ids(
    api_client: Client,
) -> None:
    response = api_client.get("/api/gurus/")
    response_json = response.json()

    item_ids = [item.get("id") for item in response_json.get("items")]

    assert response.status_code == HTTPStatus.OK
    assert len(item_ids) == len(set(item_ids))
    Page[Guru].model_validate(response_json)


@pytest.mark.parametrize("page, size", [(1, 5), (2, 3), (1, 10)])
def test_get_gurus_list_pagination_should_be_successful(
    api_client: Client,
    page: int,
    size: int,
) -> None:
    """Проверяет корректную работу пагинации."""
    response = api_client.get(f"/api/gurus/?page={page}&size={size}")
    assert response.status_code == HTTPStatus.OK

    response_json = response.json()
    Page[Guru].model_validate(response_json)

    assert response_json["page"] == page
    assert response_json["size"] == size
    assert len(response_json["items"]) <= size


@pytest.mark.parametrize("page, size", [(0, 5), (-1, 5), (1, 0), (1, -1), (1, 101)])
def test_get_gurus_list_invalid_pagination_params_should_return_unprocessable_entity(
    api_client: Client, page: int, size: int
) -> None:
    """Проверяет обработку некорректных параметров пагинации."""
    response = api_client.get(f"/api/gurus/?page={page}&size={size}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
