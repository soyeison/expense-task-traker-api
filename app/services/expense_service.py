from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from app.schemas.expense_schema import (
    ExpenseCreateSchema,
    ExpenseSchemaBase,
    ExpenseSchema,
)
from app.schemas.base_schema import FormatResponseSchema
from app.database.repositories.postgresql_expense_repository import (
    PostgreSqlExpenseRepository,
)


class ExpenseService:
    def __init__(
        self,
        expense_repository: PostgreSqlExpenseRepository = Depends(
            PostgreSqlExpenseRepository
        ),
    ):
        self.expense_repo = expense_repository

    def create_expense(self, user_id: int, expense: ExpenseCreateSchema):
        expense_schema_base = ExpenseSchemaBase(**expense.__dict__, user_id=user_id)
        expense_created = self.expense_repo.create(expense=expense_schema_base)

        expense_response_schema = ExpenseSchema(**expense_created.__dict__)

        response_schema = FormatResponseSchema(
            data=jsonable_encoder(expense_response_schema),
            message="Expense created correctly",
        )

        return jsonable_encoder(response_schema)

    def get_by_id(self, expense_id: int):
        db_expense = self.expense_repo.get_by_id(expense_id=expense_id)

        expense_response_schema = ExpenseSchema(**db_expense.__dict__)

        response_schema = FormatResponseSchema(
            data=jsonable_encoder(expense_response_schema),
            message="Correctly obtained expense",
        )

        return jsonable_encoder(response_schema)
