import json
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from app.database.repositories.postgresql_user_repository import (
    PostgreSqlUserRepository,
)
from app.schemas.base_schema import FormatResponseSchema
from app.schemas.auth_schema import AuthSchemaBase, GetJWTAuthSchema
from app.schemas.user_schema import UserCreateSchema


class UserService:
    def __init__(
        self,
        user_repository: PostgreSqlUserRepository = Depends(PostgreSqlUserRepository),
    ) -> None:
        self.user_repo = user_repository

    def sign_up(self, payload: AuthSchemaBase):
        user_created = self.user_repo.create(payload)

        user_schema_response = GetJWTAuthSchema(
            user=jsonable_encoder(user_created), access_token=""
        )

        response_schema = FormatResponseSchema(
            data=jsonable_encoder(user_schema_response),
            message="Usuario registrado correctamente",
        )

        repsonse_dict = jsonable_encoder(response_schema)

        return repsonse_dict
