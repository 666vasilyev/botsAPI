from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.crud import get_all_bots, get_bot_by_id, add_bot, update_bot, delete_bot
from src.models import BasicBotsModel, ReqBotsModel, Data
from src.db.session import get_session_dep

router = APIRouter(prefix="/bot")


@router.get("/")
async def get_bots(session: Annotated[AsyncSession, Depends(get_session_dep)]):
    return await get_all_bots(session)


@router.get("/bot_id}")
async def get_bot(
    bot_id: int, session: Annotated[AsyncSession, Depends(get_session_dep)]
):
    return await get_bot_by_id(bot_id, session)


@router.post("/")
async def post_bots(
    collect_model: BasicBotsModel,
    session: Annotated[AsyncSession, Depends(get_session_dep)],
):
    new_bot = await add_bot(collect_model, session)
    return ReqBotsModel(
        status="ok", data=Data(id=new_bot, new=new_bot is not None)
    )


@router.patch("/bot_id}")
async def patch_bots(
    bot_id: int,
    collect_model: BasicBotsModel,
    session: Annotated[AsyncSession, Depends(get_session_dep)],
):
    return await update_bot(bot_id, collect_model, session)


@router.delete("/{bot_id}")
async def delete_bots(
    bot_id: int, session: Annotated[AsyncSession, Depends(get_session_dep)]
):
    return await delete_bot(bot_id, session)
