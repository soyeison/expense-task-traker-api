from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app.schemas.expense_schema import ExpenseSchemaBase, ExpenseUpdateSchema
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

    def get_expense_by_id(self, expense_id: int):
        db_expense = (
            self.db.query(ExpenseModel).filter(ExpenseModel.id == expense_id).first()
        )

        return db_expense

    def update_expense(
        self, expense_id: int, expense: ExpenseUpdateSchema
    ) -> ExpenseModel | None:
        db_expense = self.get_expense_by_id(expense_id=expense_id)
        for attr, value in expense.model_dump(exclude_unset=True).items():
            setattr(db_expense, attr, value)
        self.db.add(db_expense)
        self.db.commit()
        self.db.refresh(db_expense)
        return db_expense

    def delete_expense(self, expense_id: int):
        db_expense = self.get_expense_by_id(expense_id=expense_id)

        self.db.delete(db_expense)
        self.db.commit()
        return db_expense
