from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from typing import List, TYPE_CHECKING, Type


def get_model_required_fields(
    model: SQLModel | BaseModel | Type[SQLModel] | Type[BaseModel],
) -> List[str]:
    return [field_name for field_name, field_info in model.model_fields.items() if field_info.is_required()]

def get_model_fields(
    model: SQLModel | BaseModel | Type[SQLModel] | Type[BaseModel],
) -> List[str]:
    return [field_name for field_name, field_info in model.model_fields.items()]
