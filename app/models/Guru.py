from typing import List, TYPE_CHECKING
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .Quote import Quote


class GuruBase(SQLModel):
    name: str
    email: EmailStr
    url: str


class Guru(GuruBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    quotes: List["Quote"] = Relationship(back_populates="guru")


class GuruCreate(GuruBase):
    pass


class GuruUpdate(SQLModel):
    name: str | None = None
    email: EmailStr | None = None
    url: str | None = None
