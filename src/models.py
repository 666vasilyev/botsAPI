<<<<<<< HEAD
from pydantic import BaseModel
from typing import Optional


class BasicBotsModel(BaseModel):
    alias: str
    description: str
    token: str
    name: str
=======
from typing import Optional

from pydantic import BaseModel
>>>>>>> 5d8c2b0 (adding new version with tests and starlette-admin)


class Data(BaseModel):
    id: int | None
    new: bool


<<<<<<< HEAD
class ReqBotsModel(BaseModel):
    status: str
    data: Data


=======
>>>>>>> 5d8c2b0 (adding new version with tests and starlette-admin)
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
<<<<<<< HEAD
=======
    bot_id: int
>>>>>>> 5d8c2b0 (adding new version with tests and starlette-admin)
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
    channel: str
    bot_id: int
    bundle: bool
    message: str


class AllBundlesModel(BaseModel):
    all_bundles: list[BundleModel]
