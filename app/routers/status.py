# app/routers/status.py

from fastapi.routing import APIRouter
from http import HTTPStatus

from app.db.engine import check_availability
from app.models.AppStatus import AppStatus

router = APIRouter(prefix="/status", tags=["Status"])


@router.get(
    "/",
    summary="Проверить статус работы API",
    status_code=HTTPStatus.OK,
    response_model=AppStatus,
)
def get_app_status() -> AppStatus:
    """
    Проверяет, загружены ли данные, и возвращает статус приложения.
    """
    return AppStatus(is_db_available=check_availability())
