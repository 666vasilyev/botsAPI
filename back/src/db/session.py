import contextlib

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.core.config import config

engine = create_async_engine(config.db_url("postgresql+asyncpg"))

async_session = async_sessionmaker(engine, expire_on_commit=False, autoflush=True)


async def get_session_dep() -> AsyncSession:
    async with async_session() as session:
        yield session


get_session = contextlib.asynccontextmanager(get_session_dep)