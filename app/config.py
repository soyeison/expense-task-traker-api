from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    debug: bool = False
    database_url: str
    jwt_private_key: str
    access_token_expire_minutes: int

    class ConfigDict:
        env_file = ".env"


settings = Settings()
