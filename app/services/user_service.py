import json
from fastapi.responses import JSONResponse
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from app.database.repositories.postgresql_user_repository import (
    PostgreSqlUserRepository,
)
from app.schemas.base_schema import FormatResponseSchema
from app.schemas.auth_schema import AuthSchemaBase, GetJWTAuthSchema
from app.schemas.user_schema import UserCreateSchema, UserSchema
from app.utils.auth.jwt import create_token
from app.utils.auth.hash_password import hash_password
from app.utils.auth.hash_password import verify_password


class UserService:
    def __init__(
        self,
        user_repository: PostgreSqlUserRepository = Depends(PostgreSqlUserRepository),
    ) -> None:
        self.user_repo = user_repository

    def sign_up(self, payload: AuthSchemaBase):
        user = self.user_repo.get_user_by_username(username=payload.username)

        if user is not None:
            response_schema = FormatResponseSchema(
                data=None,
                message="El usuario ya existe",
            )

            return jsonable_encoder(response_schema)

        # Guardar el password encriptado
        hashed_password = hash_password(payload.password)
        setattr(payload, "password", hashed_password)

        user_created = self.user_repo.create(payload)

        user_response_schema = UserSchema(**user_created.__dict__)

        response_schema = FormatResponseSchema(
            data=jsonable_encoder(user_response_schema),
            message="Usuario registrado correctamente",
        )

        repsonse_dict = jsonable_encoder(response_schema)

        return repsonse_dict

    def login(self, payload: AuthSchemaBase):
        user = self.user_repo.get_user_by_username(username=payload.username)

        if user is None:
            response_schema = FormatResponseSchema(
                data=None,
                message="El usuario no existe",
            )

            return jsonable_encoder(response_schema)

        if (
            verify_password(
                plain_passsword=payload.password, hashed_password=user.password
            )
            == False
        ):
            response_schema = FormatResponseSchema(
                data=None,
                message="El password es incorrecto",
            )

            return jsonable_encoder(response_schema)

        user_schema_response = GetJWTAuthSchema(
            user=jsonable_encoder(user),
            access_token=create_token({"user_id": str(user.id)}),
        )

        response_schema = FormatResponseSchema(
            data=jsonable_encoder(user_schema_response),
            message="Usuario encontrado correctamente",
        )

        repsonse_dict = jsonable_encoder(response_schema)

        return repsonse_dict
