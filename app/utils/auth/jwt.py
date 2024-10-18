import jwt
from app.config import settings


def create_token(data: dict):
    token: str = jwt.encode(
        payload=data, key=settings.jwt_private_key, algorithm="HS256"
    )
    return token
