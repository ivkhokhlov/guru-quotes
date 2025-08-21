from typing import List

from pydantic import BaseModel, EmailStr, HttpUrl


class Quote(BaseModel):
    id: int
    text: str


class Guru(BaseModel):
    id: int
    name: str
    email: EmailStr
    url: HttpUrl
    quotes: List[Quote]
