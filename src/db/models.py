import datetime
from typing import List

from sqlalchemy import String, text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Bot(Base):
    __tablename__ = "Bots"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    alias: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    bot_token: Mapped[str] = mapped_column(nullable=False, unique=True)
    channels: Mapped[List[str]] = mapped_column(ARRAY(String))
    channels_count: Mapped[int] = mapped_column(default=0)


class ChannelBot(Base):
    __tablename__ = "ChannelBotBundles"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    channel: Mapped[str] = mapped_column(nullable=False)
    bot_id: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("NOW()"))
    bundle: Mapped[bool] = mapped_column(nullable=False)
    message: Mapped[str] = mapped_column(default="Bundle is active")
