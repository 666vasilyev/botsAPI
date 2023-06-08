import logging
from typing import Sequence

import asyncpg
from fastapi import HTTPException
from sqlalchemy import select, update, func, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.db.models import Bot, ChannelBot
from src.db.session import get_session
from src.models import (
    BasicBotsModel,
    StatusModel,
    ChannelListModel,
    BotAliasByChannelIdModel,
    AllBundlesModel,
    BundleModel,
)

logger = logging.getLogger(__name__)


async def add_bot(bot_data: BasicBotsModel, session: AsyncSession):
    new_bot = Bot(
        alias=bot_data.alias,
        description=bot_data.description,
        name=bot_data.name,
        bot_token=bot_data.token,
        channels=[],
    )
    session.add(new_bot)
    try:
        await session.commit()
        await session.refresh(new_bot)
    except asyncpg.exceptions.UniqueViolationError:
        await session.rollback()
    finally:
        return new_bot.id
    # TODO: лучше без finally и возвращать всего бота, а не только айди


async def get_all_bots(session: AsyncSession) -> Sequence[Bot]:
    stmt = select(Bot)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_bot_by_id(bot_id: int, session: AsyncSession) -> Bot:
    bot = await session.execute(select(Bot).filter_by(id=bot_id))
    result = bot.scalar()
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no bot with the specified id",
        )
    return result


async def update_bot(bot_id: int, update_data: BasicBotsModel, session: AsyncSession):
    bot = await session.get(Bot, bot_id)
    if bot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no bot with the specified id",
        )
    for field, value in update_data:
        setattr(bot, field, value)
    try:
        await session.commit()
        await session.refresh(bot)
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    raise HTTPException(
        status_code=status.HTTP_200_OK, detail="Bot successfully updated"
    )


async def delete_bot(bot_id: int, session: AsyncSession):
    bot = await session.get(Bot, bot_id)
    delete_query = delete(ChannelBot).where(ChannelBot.bot_id == bot_id)
    if bot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no bot with the specified id",
        )
    await session.delete(bot)
    await session.execute(delete_query)
    try:
        await session.commit()
        return StatusModel(status="Success")
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


async def add_channel_to_bot_by_bot_id(bot_id: int, channel: str):
    async with get_session() as session:
        async with session.begin():
            # Проверяем, существует ли уже канал в списке каналов бота
            existing_channel = await session.execute(
                select(Bot)
                .where(Bot.id == bot_id)
                .where(Bot.channels.contains([channel]))
            )
            if existing_channel.scalar_one_or_none():
                return StatusModel(status="Channel already exists")

            try:
                # Обновляем запись бота и добавляем новый канал
                query = (
                    update(Bot)
                    .where(Bot.id == bot_id)
                    .values(
                        channels=Bot.channels + [channel],
                        channels_count=Bot.channels_count + 1,
                    )
                )
                await session.execute(query)

                # Добавляем новую связь между каналом и ботом
                await add_new_bundle(channel=channel, bot_id=bot_id, session=session)

                return StatusModel(status="Success")
            except IntegrityError:
                return StatusModel(status="Channel already exists")
            except Exception as e:
                return StatusModel(status="Error: " + str(e))


async def add_new_bundle(bot_id: int, channel: str, session: AsyncSession):
    new_bundle = ChannelBot(channel=channel, bot_id=bot_id, bundle=True)
    session.add(new_bundle)
    try:
        await session.commit()
        await session.refresh(new_bundle)
        return StatusModel(status="Success")
    except Exception as e:
        return StatusModel(status="Error: " + str(e))


async def remove_channel_from_bot(bot_id: int, channel: str, session: AsyncSession):
    bot = await session.get(Bot, bot_id)
    if bot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no bot with the specified id",
        )
    if channel not in bot.channels:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The channel {channel} does not exist in the bot's channels",
        )
    query = (
        update(Bot)
        .where(Bot.id == bot_id)
        .values(channels=func.array_remove(Bot.channels, channel))
    )
    delete_query = (
        delete(ChannelBot)
        .where(ChannelBot.channel == channel)
        .where(ChannelBot.bot_id == bot_id)
    )
    await session.execute(query)
    await session.execute(delete_query)
    try:
        await session.commit()
        return StatusModel(status="Success")
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


async def get_all_channels(session: AsyncSession):
    query = select(func.unnest(Bot.channels).distinct().label("channel"))
    result = await session.execute(query)
    channels = [row[0] for row in result]
    if not channels:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No channels found"
        )
    return ChannelListModel(channels=channels)


async def get_bot_token_by_channel_id(channel_id: str, session: AsyncSession):
    query = select(Bot.bot_token).where(Bot.channels.op("@>")([channel_id]))
    result = await session.execute(query)
    row = result.scalar_one_or_none()
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No bot found with that channel_id",
        )
    return row


async def get_bot_url_by_channel_id(channel_id: str, session: AsyncSession):
    query = select(Bot.alias).where(Bot.channels.op("@>")([channel_id]))
    result = await session.execute(query)
    row = result.scalar_one_or_none()
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No bot found with that channel_id",
        )
    return BotAliasByChannelIdModel(alias=row)


async def get_bot_with_min_channels_count(session: AsyncSession):
    query = select(Bot).order_by(Bot.channels_count).limit(1)
    result = await session.execute(query)
    row = result.fetchone()
    if row:
        return row[0]
    return None


async def set_bundle_status(
    bot_id: str, channel: str, bundle_status: bool, message: str, session: AsyncSession
):
    update_query = (
        update(ChannelBot)
        .where(ChannelBot.channel == channel)
        .where(ChannelBot.bot_id == bot_id)
        .values(bundle=bundle_status, message=message)
    )
    await session.execute(update_query)
    await session.commit()


async def get_bot_id_by_token(session: AsyncSession, bot_token):
    query = select(Bot.id).where(Bot.bot_token == bot_token)
    row = await session.execute(query)
    bot_id = row.fetchone()
    return bot_id[0]


async def get_all_bundles(session: AsyncSession):
    res = AllBundlesModel(all_bundles=[])
    result = await session.execute(select(ChannelBot))
    records = result.scalars().all()
    for record in records:
        bundle = BundleModel(
            channel=record.channel,
            bot_id=record.bot_id,
            bundle=record.bundle,
            message=record.message,
        )
        res.all_bundles.append(bundle)
    return res
