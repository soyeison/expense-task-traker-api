from fastapi import FastAPI
from app.controllers.auth_controller import AuthController
from app.database.db import init_db

app = FastAPI()

init_db()

auth_controller = AuthController()

app.include_router(auth_controller.router, prefix="/api/v1/auth", tags=["Auth"])
