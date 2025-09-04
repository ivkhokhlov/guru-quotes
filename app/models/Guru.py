from typing import List, TYPE_CHECKING
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .Quote import Quote


class Guru(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: EmailStr
    url: str

    quotes: List["Quote"] = Relationship(back_populates="guru")
