# uvicorn main:app --host 0.0.0.0 --port 8000  --reload
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles

# from src.db.session import sessionmanager
from src.middlewares import AuthMiddleware
from src.routers import bot_router, channel_router, messages_router, task_router, admin_router

logger = logging.getLogger(__name__)


def get_app(init_db: bool = True):
    lifespan = None

    # if init_db:
    #     sessionmanager.init(config.db_url("postgresql+asyncpg"))

    #     @asynccontextmanager
    #     async def lifespan(app: FastAPI):
    #         yield
    #         if sessionmanager._engine is not None:
    #             await sessionmanager.close()

    app = FastAPI(title="botsAPI", lifespan=lifespan)

    @app.on_event("startup")
    async def startup():
        logging.basicConfig(level=logging.INFO)

    app.include_router(bot_router)
    app.include_router(task_router)
    app.include_router(channel_router)
    app.include_router(messages_router)

    app.mount("/statics", StaticFiles(directory="statics"), name="statics")
    app.include_router(admin_router)
    app.add_middleware(AuthMiddleware)
    app.add_middleware(SessionMiddleware, secret_key='jopa')

    return app
