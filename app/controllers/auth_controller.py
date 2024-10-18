from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.services.user_service import UserService
from app.schemas.auth_schema import AuthSchemaBase
from app.schemas.base_schema import FormatResponseSchema


class AuthController:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.post("/sign-up", response_model=FormatResponseSchema)(self.sign_up)
        self.router.post("/login", response_model=FormatResponseSchema)(self.login)

    async def sign_up(
        self, payload: AuthSchemaBase, user_service: UserService = Depends(UserService)
    ):
        response = user_service.sign_up(payload)

        return JSONResponse(content=response, status_code=201)

    async def login(
        self, payload: AuthSchemaBase, user_service: UserService = Depends(UserService)
    ):
        response = user_service.login(payload)

        return JSONResponse(content=response, status_code=200)
