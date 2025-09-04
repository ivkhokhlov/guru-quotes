from typing import Sequence
from app.models.Guru import Guru, GuruUpdate
from .engine import engine
from sqlmodel import Session, select


def get_guru_by_id(guru_id: int) -> Guru | None:
    with Session(engine) as session:
        return session.get(Guru, guru_id)


def get_all_gurus() -> Sequence[Guru]:
    with Session(engine) as session:
        statement = select(Guru)
        return session.exec(statement).all()


def create_guru(guru: Guru) -> Guru:
    with Session(engine) as session:
        session.add(guru)
        session.commit()
        session.refresh(guru)
        return guru


def patch_guru(guru_id: int, guru_update: GuruUpdate) -> Guru | None:
    """
    Частично обновляет данные гуру.
    Обновляются только те поля, которые были переданы.
    """
    with Session(engine) as session:
        db_guru = session.get(Guru, guru_id)
        if not db_guru:
            return None

        update_data = guru_update.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_guru, key, value)

        session.add(db_guru)
        session.commit()
        session.refresh(db_guru)

        return db_guru



def delete_guru(guru_id: int) -> Guru | None:
    with Session(engine) as session:
        guru_to_delete = session.get(Guru, guru_id)
        if not guru_to_delete:
            return None

        if guru_to_delete.quotes:
            raise ValueError(f"Нельзя удалить гуру '{guru_to_delete.name}', так как у него есть цитаты.")

        session.delete(guru_to_delete)
        session.commit()
        return guru_to_delete
