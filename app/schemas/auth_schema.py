from pydantic import BaseModel
from app.schemas.user_schema import UserSchema


class AuthSchemaBase(BaseModel):
    username: str
    password: str


class GetJWTAuthSchema(BaseModel):
    user: UserSchema
    access_token: str
