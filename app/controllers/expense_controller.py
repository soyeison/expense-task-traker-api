from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.services.user_service import UserService
from app.schemas.auth_schema import AuthSchemaBase, SignUpSchema
from app.schemas.base_schema import FormatResponseSchema


class ExpenseController:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get("/", response_model=FormatResponseSchema)(self.get_all)
        self.router.get("/{expense_id}", response_model=FormatResponseSchema)(
            self.get_by_id
        )
        self.router.post("/", response_model=FormatResponseSchema)(self.create)

    async def get_all(self):
        pass

    async def get_by_id(self):
        pass

    async def create(self):
        pass
