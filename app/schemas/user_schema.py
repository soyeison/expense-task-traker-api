from datetime import datetime
from typing import Union
from pydantic import BaseModel


class UserSchemaBase(BaseModel):
    username: str

    class ConfigDict:
        orm_mode = True


class UserSchema(UserSchemaBase):
    id: int
    created_at: Union[str, datetime]
    updated_at: Union[str, datetime]


class UserCreateSchema(UserSchemaBase):
    pass
