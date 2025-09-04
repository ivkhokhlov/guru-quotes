from pydantic import BaseModel


class AppStatus(BaseModel):
    status: str
