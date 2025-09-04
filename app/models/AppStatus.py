from pydantic import BaseModel


class AppStatus(BaseModel):
    is_db_available: bool
