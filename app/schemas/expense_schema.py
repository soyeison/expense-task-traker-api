from datetime import datetime
from typing import Union
from pydantic import BaseModel


class ExpenseSchemaBase(BaseModel):
    description: str
    amount: float
    category_id: int
    user_id: int

    class ConfigDict:
        orm_mode = True


class ExpenseSchema(ExpenseSchemaBase):
    id: int
    user_id: int
    created_at: Union[str, datetime]
    updated_at: Union[str, datetime]


class ExpenseCreateSchema(BaseModel):
    description: str
    amount: float
    category_id: int

    class ConfigDict:
        orm_mode = True


class ExpenseUpdateSchema(ExpenseCreateSchema):
    description: Union[str, None] = None
    amount: Union[float, None] = None
    category_id: Union[int, None] = None
