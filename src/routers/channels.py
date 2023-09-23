from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.celery import celery_tasks
from src.db.crud import (
    get_all_bundles,
    get_bot_by_channel_id,
    get_bot_with_min_channels_count,
    remove_channel_from_bot,
)
from src.db.session import get_session
from src.models import (
    BotAliasByChannelIdModel,
    ChannelPostReqModel,
    ChannelPostResModel,
    ChannelPostResModelByBotId,
    TaskIdModel,
)

router = APIRouter(prefix="/channel")


@router.get("/")
async def get_channels(session: Annotated[AsyncSession, Depends(get_session)]):
    return await get_all_bundles(session)


@router.get("/{channel_id}")
async def get_channels_by_id(
    channel_id: str, session: Annotated[AsyncSession, Depends(get_session)]
):
    bot = await get_bot_by_channel_id(session=session, channel_id=channel_id)
    return BotAliasByChannelIdModel(alias=bot.alias) 


@router.post("/")
async def post_channels(
    collect_model: ChannelPostResModelByBotId,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    if collect_model.bot_id:
        celery_task = celery_tasks.sync_add_channel_to_bot_by_bot_id.delay(
            bot_id=collect_model.bot_id, channel=collect_model.channel
        )
        return TaskIdModel(task_id=celery_task.id)
    else:
        row = await get_bot_with_min_channels_count(session)
        return ChannelPostReqModel(
            channel_id=collect_model.channel,
            bot_link=f"@{row.name}",
            message="Канал добавлен, для дальнейшей работы необходимо дать боту права "
            "администратора в текущем канале",
        )


@router.delete("/{bot_id}")
async def delete_channels(
    bot_id: int,
    collect_model: ChannelPostResModel,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    return await remove_channel_from_bot(
        bot_id=bot_id, channel=collect_model.channel, session=session
    )
