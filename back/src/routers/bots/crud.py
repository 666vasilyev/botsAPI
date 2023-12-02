from typing import Sequence

import asyncpg
from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.db.models import Bot, ChannelBot
from src.routers.bots.models import BotCreate, BotUpdate


async def add_bot(bot_data: BotCreate, session: AsyncSession):
    new_bot = Bot(
        alias=bot_data.alias,
        description=bot_data.description,
        name=bot_data.name,
        bot_token=bot_data.bot_token,
        channels=[],
    )
    session.add(new_bot)
    try:
        await session.commit()
        await session.refresh(new_bot)
        return new_bot
    except asyncpg.exceptions.UniqueViolationError:
        await session.rollback()


async def get_all_bots(session: AsyncSession) -> Sequence[Bot]:
    return (await session.execute(select(Bot))).scalars().fetchall()


async def get_bot_by_id(bot_id: int, session: AsyncSession) -> Bot:
    bot = await session.execute(select(Bot).filter_by(id=bot_id))
    result = bot.scalar()
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no bot with the specified id",
        )
    return result


async def update_bot(bot_id: int, update_data: BotUpdate, session: AsyncSession):
    bot = await session.get(Bot, bot_id)
    if bot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no bot with the specified id",
        )
    for field, value in update_data.dict(exclude_none=True).items():
        setattr(bot, field, value)
    try:
        await session.commit()
        await session.refresh(bot)
        return bot
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
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
        return bot
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
