import json
from pathlib import Path
from sqlmodel import Session, select
from app.db.engine import engine
from app.models.Guru import Guru
from app.models.Quote import Quote


DATA_FILE_PATH = Path(__file__).parent.parent.parent / "guru_quotes" / "gurus.json"


def seed_database():
    with Session(engine) as session:
        # Проверяем, есть ли уже гуру в базе, чтобы не дублировать данные при перезапуске
        statement = select(Guru)
        results = session.exec(statement).all()
        if results:
            print("INFO:     Database already seeded. Skipping.")
            return

        print("INFO:     Seeding database with initial data...")
        with open(DATA_FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            gurus_to_add = []
            for guru_data in data:
                # Отделяем данные цитат от данных гуру
                quotes_data = guru_data.pop("quotes", [])
                guru = Guru(**guru_data)

                # Создаем объекты Quote и сразу привязываем их к объекту Guru
                # SQLModel автоматически подставит guru_id при сохранении.
                quotes_for_guru = [Quote(text=q["text"]) for q in quotes_data]
                guru.quotes = quotes_for_guru
                gurus_to_add.append(guru)

            session.add_all(gurus_to_add)
            session.commit()
        print("INFO:     Database seeding complete.")
