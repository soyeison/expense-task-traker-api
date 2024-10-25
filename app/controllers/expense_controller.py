from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import Annotated
from app.services.expense_service import ExpenseService
from app.schemas.expense_schema import ExpenseCreateSchema
from app.schemas.expense_schema import ExpenseUpdateSchema
from app.schemas.base_schema import FormatResponseSchema
from app.utils.auth.jwt import get_current_user
from app.database.models.user_model import UserModel


class ExpenseController:
    def __init__(self) -> None:
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.get("/", response_model=FormatResponseSchema)(self.get_all)
        self.router.get(
            "/{expense_id}",
            response_model=FormatResponseSchema,
            dependencies=[Depends(get_current_user)],
        )(self.get_by_id)
        self.router.post(
            "/",
            response_model=FormatResponseSchema,
            dependencies=[Depends(get_current_user)],
        )(self.create)
        self.router.put(
            "/{expense_id}",
            response_model=FormatResponseSchema,
            dependencies=[Depends(get_current_user)],
        )(self.update_expense)
        self.router.delete(
            "/{expense_id}",
            response_model=FormatResponseSchema,
            dependencies=[Depends(get_current_user)],
        )(self.delete_expense)

    async def get_all(self):
        pass

    async def get_by_id(
        self, expense_id: int, expense_service: ExpenseService = Depends(ExpenseService)
    ):
        response = expense_service.get_by_id(expense_id=expense_id)

        return JSONResponse(content=response, status_code=200)

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

    async def update_expense(
        self,
        expense_id: int,
        expense: ExpenseUpdateSchema,
        expense_service: ExpenseService = Depends(ExpenseService),
    ):
        response = expense_service.update_expense(
            expense_id=expense_id, expense=expense
        )

        return JSONResponse(content=response, status_code=200)

    async def delete_expense(
        self, expense_id: int, expense_service: ExpenseService = Depends(ExpenseService)
    ):
        response = expense_service.deelete_expense(expense_id=expense_id)

        return JSONResponse(content=response, status_code=200)
