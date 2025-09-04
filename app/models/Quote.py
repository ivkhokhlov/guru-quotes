from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .Guru import Guru

class QuoteBase(SQLModel):
    text: str
    guru_id: int | None = Field(default=None, foreign_key="guru.id")

class Quote(QuoteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    guru: Optional["Guru"] = Relationship(back_populates="quotes")

class QuoteRead(QuoteBase):
    id: int
