from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str
    TEST_DB_URL: str
    MODE: Literal["DEV", "TEST"]

    class Config:
        env_file = ".env"


settings = Settings()