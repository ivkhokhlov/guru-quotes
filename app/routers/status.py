from fastapi.routing import APIRouter
from http import HTTPStatus
from sqlmodel import Session, select
from sqlalchemy.exc import OperationalError

from app.models.AppStatus import AppStatus
from app.db.engine import engine # Импортируем engine для соединения с БД

router = APIRouter(
    prefix="/status",
    tags=["Status"]
)

@router.get(
    '/',
    summary='Проверить статус работы API',
    status_code=HTTPStatus.OK,
    response_model=AppStatus
)
def get_app_status() -> AppStatus:
    """
    Проверяет доступность базы данных и возвращает статус приложения.
    """
    try:
        # Попытка выполнить простой запрос к БД
        with Session(engine) as session:
            session.exec(select(1))
        current_status = 'OK'
    except OperationalError:
        # Если не удалось подключиться, будет эта ошибка
        current_status = 'DATABASE_OFFLINE'

    return AppStatus(status=current_status)
