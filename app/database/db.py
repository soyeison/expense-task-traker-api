from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

SQLALCHEMY_DATABASE_URL = settings.database_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from app.database.models.user_model import UserModel
    from app.database.models.category_model import CategoryModel
    from app.database.models.expense_model import ExpenseModel

    # Crear las tablas de la base de datos
    Base.metadata.create_all(bind=engine)
