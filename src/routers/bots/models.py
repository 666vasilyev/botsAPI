from pydantic import BaseModel, Field


class BotRead(BaseModel):
    id: int = Field(default=0)
    alias: str
    description: str
    name: str
    bot_token: str
    channels: list[str] = Field(default_factory=list)
    channels_count: int = Field(default=0)

    class Config:
        orm_mode = True


class BotCreate(BaseModel):
    alias: str
    description: str
    name: str
    bot_token: str


class BotUpdate(BaseModel):
    alias: str | None
    description: str | None
    name: str | None
    bot_token: str | None
    channels: list[str] | None
    channels_count: int | None

class BundleStatusModel(BaseModel):
    bot_id: int
    channel_id: str
    is_admin: bool
    message: str