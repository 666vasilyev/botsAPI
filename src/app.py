# uvicorn main:app --host 0.0.0.0 --port 8000  --reload
import logging

from fastapi import Depends, FastAPI
from fastapi_users import FastAPIUsers
from fastapi.middleware.cors import CORSMiddleware

from src.db.models import User
from src.core.auth.auth import auth_backend
from src.core.auth.manager import get_user_manager
from src.core.auth.schemas import UserRead, UserCreate
from src.routers import bot_router, channel_router, messages_router, task_router, activity_router

logger = logging.getLogger(__name__)



def get_app(init_db: bool = True):
    """Create the FastAPI application."""

    lifespan = None

    app = FastAPI(title="botsAPI", lifespan=lifespan)

    origins = [
        "http://localhost.tiangolo.com",
        "https://localhost.tiangolo.com",
        "http://localhost",
        "http://localhost:8080",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    async def startup():
        logging.basicConfig(level=logging.INFO)

    fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend], )
    app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"], )
    app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"], )

    current_user = fastapi_users.current_user()

    app.include_router(bot_router, dependencies=[Depends(current_user)])
    app.include_router(task_router, dependencies=[Depends(current_user)])
    app.include_router(channel_router, dependencies=[Depends(current_user)])
    app.include_router(messages_router, dependencies=[Depends(current_user)])
    app.include_router(activity_router, dependencies=[Depends(current_user)])

    return app
