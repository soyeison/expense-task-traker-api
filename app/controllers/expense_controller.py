from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import Annotated
from app.services.expense_service import ExpenseService
from app.schemas.expense_schema import ExpenseCreateSchema
from app.schemas.base_schema import FormatResponseSchema
from app.utils.auth.jwt import get_current_user
from app.database.models.user_model import UserModel


class ExpenseController:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get("/", response_model=FormatResponseSchema)(self.get_all)
        self.router.get("/{expense_id}", response_model=FormatResponseSchema)(
            self.get_by_id
        )
        self.router.post(
            "/",
            response_model=FormatResponseSchema,
            dependencies=[Depends(get_current_user)],
        )(self.create)

    async def get_all(self):
        pass

    async def get_by_id(self):
        pass

    async def create(
        self,
        current_user: Annotated[UserModel, Depends(get_current_user)],
        expense: ExpenseCreateSchema,
        expense_service: ExpenseService = Depends(ExpenseService),
    ):
        response = expense_service.create_expense(
            user_id=current_user.id, expense=expense
        )

        return JSONResponse(content=response, status_code=201)
