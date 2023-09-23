import pytest_asyncio

from src.core.config import config
from src.db.crud import add_channel_to_bot_by_bot_id
from src.db.models import Bot
from src.routers.bots.crud import add_bot, delete_bot
from src.db.session import get_session, sessionmanager
from src.routers.bots.models import BotCreate


@pytest_asyncio.fixture(autouse=True)
async def init_database_manager():
    sessionmanager.init(config.db_url("postgresql+asyncpg"))

    yield

    await sessionmanager.close()


@pytest_asyncio.fixture
async def fill_test_database() -> Bot:
    # Инициализация тестовых данных
    bot_id = 0
    bot_token = "123:123"
    bot_name = "test_bot"
    bot_description = "test_bot"
    bot_alias = "test_bot"
    async with sessionmanager.session() as session:
        bot_id = (await add_bot(session=session,
                                bot_data=BotCreate(
                                    bot_token=bot_token,
                                    name=bot_name,
                                    description=bot_description,
                                    alias=bot_alias
                                ))).id
        await add_channel_to_bot_by_bot_id(bot_id=bot_id, channel="test_channel")

    yield

    # Очистка тестовых данных
    async with sessionmanager.session() as session:
        await delete_bot(bot_id=bot_id, session=session)
