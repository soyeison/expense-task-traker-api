from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    debug: bool = False
    database_url: str

    class ConfigDict:
        env_file = ".env"


settings = Settings()
