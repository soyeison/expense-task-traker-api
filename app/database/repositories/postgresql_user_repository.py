from fastapi import Depends
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreateSchema
from app.database.models.user_model import UserModel
from app.database.db import get_db


class PostgreSqlUserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create(self, payload: UserCreateSchema) -> UserModel:
        db_user = UserModel(**payload.model_dump())

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user
