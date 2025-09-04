import os
from psycopg2 import OperationalError
from sqlmodel import Session, SQLModel, create_engine, text, select


engine = create_engine(
    url=os.getenv("DATABASE_ENGINE", "sqlite:///./test.db"),
    pool_size=int(os.getenv("DATABASE_POOL_SIZE", 5)),
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def check_availability():
    try:
        with Session(engine) as session:
            print(engine.url)
            print(session.exec(select(1)))
            session.exec(select(1))
            return True
    except Exception as e:
        print(e)
        return False
