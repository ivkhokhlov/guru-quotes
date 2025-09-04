from typing import Sequence
from app.models.Guru import Guru
from .engine import engine
from sqlmodel import Session, select


def get_guru_by_id(guru_id: int) -> Guru | None:
    with Session(engine) as session:
        return session.get(Guru, guru_id)


def get_all_gurus() -> Sequence[Guru]:
    with Session(engine) as session:
        statement = select(Guru)
        return session.exec(statement).all()
