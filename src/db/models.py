<<<<<<< HEAD
from typing import List

from sqlalchemy import String
=======
import datetime
from typing import List

from sqlalchemy import String, text
>>>>>>> 5d8c2b0 (adding new version with tests and starlette-admin)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Bot(Base):
<<<<<<< HEAD
    __tablename__ = "bots"
=======
    __tablename__ = "Bots"
>>>>>>> 5d8c2b0 (adding new version with tests and starlette-admin)
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    alias: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False, unique=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    bot_token: Mapped[str] = mapped_column(nullable=False, unique=True)
    channels: Mapped[List[str]] = mapped_column(ARRAY(String))
    channels_count: Mapped[int] = mapped_column(default=0)


class ChannelBot(Base):
    __tablename__ = "ChannelBotBundles"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    channel: Mapped[str] = mapped_column(nullable=False)
    bot_id: Mapped[int] = mapped_column(nullable=False)
<<<<<<< HEAD
=======
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("NOW()"))
>>>>>>> 5d8c2b0 (adding new version with tests and starlette-admin)
    bundle: Mapped[bool] = mapped_column(nullable=False)
    message: Mapped[str] = mapped_column(default="Bundle is active")
