from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./patients.db"
    SECRET_KEY: str = "change-me"


settings = Settings()