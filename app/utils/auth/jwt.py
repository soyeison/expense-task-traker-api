import jwt
from uuid import UUID
from typing import Annotated
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi import HTTPException, Request, Depends
from fastapi.security import HTTPBearer
from datetime import timedelta, datetime, timezone
from jwt.exceptions import InvalidTokenError
from app.config import settings
from app.database.repositories.postgresql_user_repository import (
    PostgreSqlUserRepository,
)


def create_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    token: str = jwt.encode(
        payload=to_encode, key=settings.jwt_private_key, algorithm="HS256"
    )
    return "Bearer" + " " + token


def validate_token(token: str) -> dict:
    try:
        data = jwt.decode(token, key="misecret", algorithms=["HS256"])
        return data
    except InvalidTokenError:
        raise HTTPException(status_code=403, detail="El token ingresado es invalido")


class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        try:
            auth = await super().__call__(request)
            # Validar que el token sea correcto
            data = validate_token(auth.credentials)
            return data
        except HTTPException:
            raise HTTPException(
                status_code=401,
                detail="El token de acceso es invalido o no se proporciono",
            )


async def get_current_user(
    user_information: Annotated[dict, Depends(BearerJWT())],
    user_repo: PostgreSqlUserRepository = Depends(PostgreSqlUserRepository),
):
    # Consultar el usuario
    user = user_repo.get_user_by_id(user_id=UUID(user_information["user_id"]))
    if user is None:
        HTTPException(status_code=401, detail="El usuario no existe")
    return user
