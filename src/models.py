import datetime
from typing import Optional

from pydantic import BaseModel


class Data(BaseModel):
    id: int | None
    new: bool


class ChannelPostResModel(BaseModel):
    channel: str


class ChannelPostResModelByBotId(BaseModel):
    channel: str
    bot_id: Optional[int] = None


class ChannelPostReqModel(BaseModel):
    channel_id: str
    bot_link: str
    message: str


class MessagesPostResModel(BaseModel):
    bot_id: int
    channel_id: str
    message: str


class TaskGetReqModel(BaseModel):
    task_id: str
    task_status: str
    task_result: str | None


class AllTasksGetReqModel(BaseModel):
    tasks: list[TaskGetReqModel]


class TaskIdModel(BaseModel):
    task_id: str


class StatusModel(BaseModel):
    status: str


class ChannelListModel(BaseModel):
    channels: list[str]


class BotAliasByChannelIdModel(BaseModel):
    alias: str


class BundleModel(BaseModel):
    id: int
    channel: str
    bot_id: int
    created_at: datetime.datetime
    bundle: bool
    message: str
    active: bool

class ActivityModel(BaseModel):
    channel: str
    active: bool


class AllBundlesModel(BaseModel):
    all_bundles: list[BundleModel]

class AllActivityModel(BaseModel):
    all_activity: list[ActivityModel]
