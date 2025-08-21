from typing import List

from pydantic import BaseModel, EmailStr


class Quote(BaseModel):
    id: int
    text: str


class Guru(BaseModel):
    id: int
    name: str
    email: EmailStr
    quotes: List[Quote]
