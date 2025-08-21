from fastapi.testclient import TestClient
import pytest
import math

from http import HTTPStatus

from guru_quotes.data import GURUS_DATA

TOTAL_GURUS = len(GURUS_DATA)


def test_get_all_gurus_default_pagination(client: TestClient) -> None:
    """Проверяет получение списка гуру с параметрами пагинации по умолчанию."""
    response = client.get("/api/gurus")
    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert "items" in response_data
    assert "total" in response_data
    assert "page" in response_data
    assert "size" in response_data
    assert "pages" in response_data
    assert response_data["page"] == 1
    assert response_data["size"] >= 1


@pytest.mark.parametrize(
    "page, size",
    [
        (1, 1),
        (2, 2),
        (1, 5),  # Размер страницы больше, чем старых данных, но меньше total
    ],
)
def test_get_gurus_pagination_success(client: TestClient, page: int, size: int) -> None:
    """Проверяет успешную работу пагинации с корректными параметрами."""
    if TOTAL_GURUS == 0:
        pytest.skip("В API нет данных для тестирования пагинации.")

    response = client.get(f"/api/gurus?page={page}&size={size}")
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert len(data["items"]) <= size
    assert data["total"] == TOTAL_GURUS
    assert data["page"] == page
    assert data["size"] == size
    assert data["pages"] == math.ceil(TOTAL_GURUS / size)


@pytest.mark.parametrize("size", [1, 3, 5, 20])
def test_pagination_pages_calculation(client: TestClient, size: int) -> None:
    """
    Проверяет, что общее количество страниц ('pages') рассчитано верно
    для разных размеров ('size').
    """
    if TOTAL_GURUS == 0:
        pytest.skip("В API нет данных.")

    response = client.get(f"/api/gurus?page=1&size={size}")
    assert response.status_code == HTTPStatus.OK
    data = response.json()

    expected_pages = math.ceil(TOTAL_GURUS / size)
    assert data["pages"] == expected_pages, (
        f"Ожидалось {expected_pages} страниц, получено {data['pages']}"
    )


def test_pagination_last_page_item_count(client: TestClient) -> None:
    """
    Проверяет, что на последней странице находится правильное количество элементов.
    """
    size = 7  # Выбираем размер, который не делит TOTAL_GURUS нацело
    if TOTAL_GURUS == 0 or TOTAL_GURUS % size == 0:
        pytest.skip(
            "Для этого теста total должен быть > 0 и не делиться на size нацело."
        )

    last_page = math.ceil(TOTAL_GURUS / size)
    response = client.get(f"/api/gurus?page={last_page}&size={size}")
    assert response.status_code == HTTPStatus.OK
    data = response.json()

    expected_item_count = TOTAL_GURUS % size
    if expected_item_count == 0:  # Если делится нацело
        expected_item_count = size

    assert len(data["items"]) == expected_item_count, (
        "Неверное количество элементов на последней странице"
    )


def test_pagination_content_uniqueness(client: TestClient) -> None:
    """
    Проверяет, что элементы на соседних страницах не пересекаются.
    """
    size = 2
    if TOTAL_GURUS <= size:
        pytest.skip("Для этого теста нужно как минимум две полные страницы.")

    response_p1 = client.get(f"/api/gurus?page=1&size={size}")
    assert response_p1.status_code == HTTPStatus.OK
    items_p1 = response_p1.json()["items"]
    ids_p1 = {item["id"] for item in items_p1}

    response_p2 = client.get(f"/api/gurus?page=2&size={size}")
    assert response_p2.status_code == HTTPStatus.OK
    items_p2 = response_p2.json()["items"]
    ids_p2 = {item["id"] for item in items_p2}

    # Проверяем, что пересечений нет
    assert not ids_p1.intersection(ids_p2), (
        "Найдены одинаковые ID на соседних страницах"
    )


def test_get_gurus_pagination_page_out_of_bounds(client: TestClient) -> None:
    """Проверяет, что запрос страницы за пределами диапазона возвращает пустой список."""
    response = client.get(f"/api/gurus?page=999&size=1")
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["items"] == []
    assert data["total"] == TOTAL_GURUS


@pytest.mark.parametrize(
    "page, size, expected_error_loc, expected_error_msg",
    [
        ("invalid", "1", ["query", "page"], "Input should be a valid integer"),
        ("1", "invalid", ["query", "size"], "Input should be a valid integer"),
        (0, 1, ["query", "page"], "Input should be greater than or equal to 1"),
        (1, 0, ["query", "size"], "Input should be greater than or equal to 1"),
        (-1, 1, ["query", "page"], "Input should be greater than or equal to 1"),
        (1, -1, ["query", "size"], "Input should be greater than or equal to 1"),
        (1.5, 1, ["query", "page"], "Input should be a valid integer"),
        (1, 1.5, ["query", "size"], "Input should be a valid integer"),
    ],
)
def test_get_gurus_pagination_invalid_params(
    client: TestClient,
    page: str,
    size: str,
    expected_error_loc: list,
    expected_error_msg: str,
) -> None:
    """Проверяет, что API возвращает ошибку 422 для невалидных параметров пагинации."""
    response = client.get(f"/api/gurus?page={page}&size={size}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    error_details = response.json()["detail"]
    assert isinstance(error_details, list)
    assert len(error_details) == 1
    assert error_details[0]["loc"] == expected_error_loc
    assert expected_error_msg in error_details[0]["msg"]
