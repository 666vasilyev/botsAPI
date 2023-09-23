# celery -A src.celery_tasks worker --loglevel=INFO --purge
# celery -A src.celery_tasks beat --loglevel=INFO
import asyncio
<<<<<<< HEAD

import logging


=======
import logging

>>>>>>> 5d8c2b0 (adding new version with tests and starlette-admin)
from aiogram import Bot, types
from celery import Celery
from fastapi import HTTPException
from redis.client import Redis
from starlette import status

<<<<<<< HEAD
from src.db.crud import (
    add_channel_to_bot_by_bot_id,
    get_bot_token_by_channel_id,
    get_session,
    get_bot_id_by_token,
    set_bundle_status,
    get_all_bots,
)
from src.models import MessagesPostResModel, StatusModel
from src.core.config import Config
=======
from src.core.config import Config
from src.db.crud import (
    add_channel_to_bot_by_bot_id,
    get_bot_id_by_token,
    get_bot_token_by_id,
    set_bundle_status,
)
from src.db.session import sessionmanager
from src.models import MessagesPostResModel, StatusModel
from src.routers.bots.crud import get_all_bots, get_bot_by_id
>>>>>>> 5d8c2b0 (adding new version with tests and starlette-admin)

celery = Celery(
    "celery_tasks",
    broker=Config().broker(),
    backend=Config().backend(),
)

celery.conf.update(
    result_backend=Config().backend(),
    beat_schedule=Config().BEAT_SCHEDULE,
)

logger = logging.getLogger(__name__)
redis = Redis(host=Config().REDIS_HOST, port=Config().REDIS_PORT, db=1)


@celery.task
def sync_celery_post_messages(request: dict):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        celery_post_messages(MessagesPostResModel.parse_obj(request))
    )


@celery.task
def sync_check_bot_status():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(check_bot_status())


@celery.task
def sync_add_channel_to_bot_by_bot_id(bot_id: int, channel: str):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(add_channel_to_bot_by_bot_id(bot_id, channel))


async def celery_post_messages(collect_model: MessagesPostResModel):
<<<<<<< HEAD
    async with get_session() as session:
        bot_token = await get_bot_token_by_channel_id(
            channel_id=collect_model.channel_id, session=session
=======
    async with sessionmanager.session() as session:
        bot_token = await get_bot_token_by_id(
            session=session,
            id=collect_model.bot_id
>>>>>>> 5d8c2b0 (adding new version with tests and starlette-admin)
        )
    bot = Bot(token=bot_token)
    try:
        await bot.send_message(
            chat_id=f"@{collect_model.channel_id}", text=collect_model.message
        )
    except Exception:
<<<<<<< HEAD
        async with get_session() as session:
            bot_id = await get_bot_id_by_token(session, bot_token)
            await set_bundle_status(bot_id, collect_model.channel_id, False, session)
        # TODO : ошибки в Celery не обрабатываются, тк все вызываемые методы - асинхронные. Разобраться.
=======
        async with sessionmanager.session() as session:
            bot_id = await get_bot_id_by_token(session, bot_token)
            await set_bundle_status(
                bot_id, collect_model.channel_id, False, collect_model.message, session
            )
        # TODO : ошибки в Celery не обрабатываются
>>>>>>> 5d8c2b0 (adding new version with tests and starlette-admin)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The bot-channel bundle is invalid",
        )
    finally:
        await bot.close()


async def check_bot_status():
<<<<<<< HEAD
    async with get_session() as session:
=======
    async with sessionmanager.session() as session:
>>>>>>> 5d8c2b0 (adding new version with tests and starlette-admin)
        bots = await get_all_bots(session)
    for bot in bots:
        if bot:
            bot_token = bot.bot_token
            channels = bot.channels
            bot_id = bot.id
            tgBot = Bot(token=bot_token)
            for channel_id in channels:
                try:
                    chat_member = await tgBot.get_chat_member(
                        f"@{channel_id}", (await tgBot.get_me()).id
                    )
                    is_admin = chat_member.status in [
                        types.ChatMemberStatus.CREATOR,
                        types.ChatMemberStatus.ADMINISTRATOR,
                    ]
<<<<<<< HEAD
                    if is_admin:
                        await set_bundle_status(
                            bot_id, channel_id, is_admin, "Bundle is active", session
                        )
                    else:
                        await set_bundle_status(
                            bot_id,
                            channel_id,
                            is_admin,
                            "Current bot doesn't have any permissions",
                            session,
                        )
=======
                    message = "Current bot doesn't have any permissions"
                    if is_admin:
                        message = "Bundle is active"
                    await set_bundle_status(
                        bot_id,
                        channel_id,
                        is_admin,
                        message,
                        session,
                    )
>>>>>>> 5d8c2b0 (adding new version with tests and starlette-admin)
                except Exception as e:
                    await set_bundle_status(bot_id, channel_id, False, str(e), session)
            await tgBot.close()
        else:
<<<<<<< HEAD
            return StatusModel(status="Bot's database is empty.")
=======
            return StatusModel(status="Bot database is empty.")
 
>>>>>>> 5d8c2b0 (adding new version with tests and starlette-admin)
