from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_session_dep

from .crud import add_bot, delete_bot, get_all_bots, get_bot_by_id, update_bot
from .models import BotCreate, BotRead, BotUpdate

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



