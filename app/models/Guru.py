from pydantic import EmailStr, HttpUrl
from sqlmodel import SQLModel, Field

from typing import List


class Guru(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: EmailStr
    # url: HttpUrl
    url: str
    # quotes: List[Quote]
