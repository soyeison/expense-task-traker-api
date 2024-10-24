from fastapi import FastAPI
from app.controllers.auth_controller import AuthController
from app.controllers.expense_controller import ExpenseController
from app.database.db import init_db

app = FastAPI()

init_db()

auth_controller = AuthController()
expense_controller = ExpenseController()

app.include_router(auth_controller.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(
    expense_controller.router, prefix="/api/v1/expense", tags=["Expense"]
)
