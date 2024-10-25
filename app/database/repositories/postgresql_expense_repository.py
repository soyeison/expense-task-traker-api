from fastapi import Depends
from sqlalchemy.orm import Session
from app.schemas.expense_schema import ExpenseSchemaBase
from app.database.models.expense_model import ExpenseModel
from app.database.db import get_db


class PostgreSqlExpenseRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create(self, expense: ExpenseSchemaBase) -> ExpenseModel:
        db_expense = ExpenseModel(**expense.model_dump())

        self.db.add(db_expense)
        self.db.commit()
        self.db.refresh(db_expense)
        return db_expense
