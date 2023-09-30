from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import User
from src.db.session import get_session_dep


async def get_user_db(session: AsyncSession = Depends(get_session_dep)):
    yield SQLAlchemyUserDatabase(session, User)