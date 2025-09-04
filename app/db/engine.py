import os
from sqlmodel import SQLModel, create_engine


engine = create_engine(
    url=os.getenv('DATABASE_ENGINE', 'sqlite:///./test.db'),
    pool_size=os.getenv('DATABASE_POOL_SIZE', 5),
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
