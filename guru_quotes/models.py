from typing import List

from pydantic import BaseModel


class Quote(BaseModel):
    id: int
    text: str


class Guru(BaseModel):
    id: int
    name: str
    quotes: List[Quote]
