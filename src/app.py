# uvicorn main:app --host 0.0.0.0 --port 8000  --reload
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette_admin.contrib.sqla import Admin, ModelView

from starlette_admin.views import Link
from starlette_admin import DropDown
from src.admin.auth import MyAuthProvider
from src.core.config import config
from src.db.session import sessionmanager
from src.routers import bot_router, channel_router, messages_router, task_router
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from src.db.models import Bot, ChannelBot

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

    app.include_router(bot_router)
    app.include_router(task_router)
    app.include_router(channel_router)
    app.include_router(messages_router)

    # Create admin
    admin = Admin(engine=sessionmanager._engine, 
                  title="Mai Bot Management",
                  auth_provider=MyAuthProvider(),
                  middlewares=[Middleware(SessionMiddleware, secret_key=config.SECRET)],)

    # Add view
    admin.add_view(
        DropDown(
            "Bots",
            views=[
                ModelView(Bot, label='List'),
            ],
        )
    )
    admin.add_view(
        DropDown(
            "Channels",
            views=[
                ModelView(ChannelBot, label='List'),
            ],
        )
    )
    admin.add_view(Link(label="Swagger API", url="/docs#"))
    # Mount admin to your app
    admin.mount_to(app)

    return app
