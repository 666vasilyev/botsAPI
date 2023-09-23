from datetime import timedelta
from typing import Literal

from pydantic import BaseSettings


class Config(BaseSettings):
    POSTGRES_HOST: str = 'localhost'
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "botsAPI"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "123"

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    SECRET: str = 'rdecs.org'

    LOG_LEVEL: str = "INFO"
    API_PORT: int = 8000
    FLOWER_PORT: int = 8888
    BEAT_SCHEDULE = {
        "sync-check-bot-status": {
            "task": "celery_tasks.sync_check_bot_status",
            "schedule": timedelta(minutes=1),
        }
    }

    def db_url(
        self,
        driver: Literal["db+postgresql", "postgresql+asyncpg", "postgresql+psycopg2"],
    ) -> str:
        return (
            f"{driver}://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}"
            f"/{self.POSTGRES_DB}"
        )

    def broker(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    def backend(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/1"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Config()
