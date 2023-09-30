from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import Bot, types
from src.db.session import get_session_dep
from starlette import status
from src.core.auth.database import User
from .crud import add_bot, delete_bot, get_all_bots, get_bot_by_id, update_bot
from .models import BotCreate, BotRead, BotUpdate, BundleStatusModel

router = APIRouter(prefix="/bot")


@router.get("/", response_model=list[BotRead])
async def get_bots(session: Annotated[AsyncSession, Depends(get_session_dep)]):
    return await get_all_bots(session)


@router.get("/{bot_id}", response_model=BotRead)
async def get_bot(bot_id: int, session: Annotated[AsyncSession, Depends(get_session_dep)]):
    return await get_bot_by_id(bot_id, session)


@router.post("/", response_model=BotRead)
async def post_bots(
    collect_model: BotCreate,
    session: Annotated[AsyncSession, Depends(get_session_dep)],
):
    return await add_bot(collect_model, session)


@router.patch("/{bot_id}", response_model=BotRead)
async def patch_bots(
    bot_id: int,
    collect_model: BotUpdate,
    session: Annotated[AsyncSession, Depends(get_session_dep)],
):
    return await update_bot(bot_id, collect_model, session)


@router.delete("/{bot_id}", response_model=BotRead)
async def delete_bots(
    bot_id: int, session: Annotated[AsyncSession, Depends(get_session_dep)]
):
    return await delete_bot(bot_id, session)



@router.get("/check_status/{bot_id}/{channel_id}")
async def check_status(
    bot_id: int, channel_id: str, session: Annotated[AsyncSession, Depends(get_session_dep)]
):
    bot = await get_bot_by_id(bot_id=bot_id, session=session)
    bot_token = bot.bot_token
    try:
        tgBot = Bot(token=bot_token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(e)
        )
    try:
        chat_member = await tgBot.get_chat_member(
            f"@{channel_id}", (await tgBot.get_me()).id
        )
        is_admin = chat_member.status in [
            types.ChatMemberStatus.CREATOR,
            types.ChatMemberStatus.ADMINISTRATOR,
        ]
        message = "Current bot doesn't have any permissions"
        if is_admin:
            message = "Bundle is active"
        await tgBot.close()
        return BundleStatusModel(
            bot_id=bot_id,
            channel_id=channel_id,
            is_admin=is_admin,
            message=message,
        )
    except Exception as e:
        await tgBot.close()
        return BundleStatusModel(
            bot_id=bot_id, 
            channel_id=channel_id, 
            is_admin=False,
            message=str(e)
        )