from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from src.db.crud import get_channel_activity, set_channel_activity
from src.db.session import get_session_dep

router = APIRouter(prefix="/activity")

@router.post("/{channel_id}")
async def post_channels_activity(
    channel_id: str,
    activity: bool,
    session: Annotated[AsyncSession, Depends(get_session_dep)]
):
    await set_channel_activity(channel_id=channel_id, activity=activity, session=session)

@router.get('/')
async def get_channels_activity(session: Annotated[AsyncSession, Depends(get_session_dep)]):
    return await get_channel_activity(session=session)