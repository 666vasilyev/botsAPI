<<<<<<< HEAD
from typing import Literal
from datetime import timedelta
=======
from datetime import timedelta
from typing import Literal

>>>>>>> 5d8c2b0 (adding new version with tests and starlette-admin)
from pydantic import BaseSettings


class Config(BaseSettings):
<<<<<<< HEAD
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "botsAPI"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: int = 123
=======
    POSTGRES_HOST: str = 'localhost'
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "botsAPI"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "123"
>>>>>>> 5d8c2b0 (adding new version with tests and starlette-admin)

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

<<<<<<< HEAD
=======
    SECRET: str = 'rdecs.org'

>>>>>>> 5d8c2b0 (adding new version with tests and starlette-admin)
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
<<<<<<< HEAD
            self,
            driver: Literal["db+postgresql", "postgresql+asyncpg", "postgresql+psycopg2"],
=======
        self,
        driver: Literal["db+postgresql", "postgresql+asyncpg", "postgresql+psycopg2"],
>>>>>>> 5d8c2b0 (adding new version with tests and starlette-admin)
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
