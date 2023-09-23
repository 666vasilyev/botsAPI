# uvicorn main:app --host 0.0.0.0 --port 8000  --reload
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_admin.app import app as admin_app
from src.core.config import config
from src.db.session import sessionmanager
from src.routers import bot_router, channel_router, messages_router, task_router


logger = logging.getLogger(__name__)


def get_app(init_db: bool = True):
    lifespan = None

    if init_db:
        sessionmanager.init(config.db_url("postgresql+asyncpg"))

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            yield
            if sessionmanager._engine is not None:
                await sessionmanager.close()

    app = FastAPI(title="botsAPI", lifespan=lifespan)

    @app.on_event("startup")
    async def startup():
        logging.basicConfig(level=logging.INFO)
        @app.on_event("startup")
        await admin_app.configure(
            providers=[
                LoginProvider(
                    admin_model=Admin,
                )
            ]
        )

    app.include_router(bot_router)
    app.include_router(task_router)
    app.include_router(channel_router)
    app.include_router(messages_router)


    return app
