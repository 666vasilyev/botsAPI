# celery -A src.celery_tasks worker --loglevel=INFO --purge
# celery -A src.celery_tasks beat --loglevel=INFO
import asyncio

import logging


from aiogram import Bot, types
from celery import Celery
from fastapi import HTTPException
from redis.client import Redis
from starlette import status

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
    async with get_session() as session:
        bot_token = await get_bot_token_by_channel_id(
            channel_id=collect_model.channel_id, session=session
        )
    bot = Bot(token=bot_token)
    try:
        await bot.send_message(
            chat_id=f"@{collect_model.channel_id}", text=collect_model.message
        )
    except Exception:
        async with get_session() as session:
            bot_id = await get_bot_id_by_token(session, bot_token)
            await set_bundle_status(bot_id, collect_model.channel_id, False, session)
        # TODO : ошибки в Celery не обрабатываются, тк все вызываемые методы - асинхронные. Разобраться.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The bot-channel bundle is invalid",
        )
    finally:
        await bot.close()


async def check_bot_status():
    async with get_session() as session:
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
                except Exception as e:
                    await set_bundle_status(bot_id, channel_id, False, str(e), session)
            await tgBot.close()
        else:
            return StatusModel(status="Bot's database is empty.")
