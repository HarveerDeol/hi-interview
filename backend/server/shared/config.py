import os
from enum import StrEnum

from dotenv import load_dotenv
from pydantic import BaseModel


class Env(StrEnum):
    TEST = "test"
    DEV = "development"
    PROD = "production"


class Config(BaseModel):
    env: Env = Env.TEST
    database_url: str = "postgresql+psycopg://hi:dev@127.0.0.1/hi_interview"
    access_token_secret_key: str = "changeme"

    @classmethod
    def from_env(cls) -> "Config":
        load_dotenv()
        return cls(
            env=Env(os.getenv("ENV", "development")),
            database_url=os.getenv(
                "DATABASE_URL", "postgresql+psycopg://hi:dev@127.0.0.1/hi_interview"
            ),
            access_token_secret_key=os.getenv(
                "ACCESS_TOKEN_SECRET_KEY", "changeme"
            ),
        )
