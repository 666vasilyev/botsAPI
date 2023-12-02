from unittest.mock import patch

import pytest
from aiogram import Bot
from aiogram.types import User, ChatMember, ChatMemberStatus

from src.core.celery.celery_tasks import celery_post_messages, check_bot_status
from src.models import MessagesPostResModel


@patch.object(Bot, "send_message")
@pytest.mark.asyncio
async def test_celery_post_messages(
        sender, fill_test_database
):
    # Подготовка входных данных
    collect_model = MessagesPostResModel(channel_id="test_channel", message="Test message")

    # Вызов функции
    try:
        await celery_post_messages(collect_model)
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")

    # Проверки
    assert sender.call_args == (
        (),
        {"chat_id": "@test_channel", "text": "Test message"}
    )


test_me = User(id="test_me")
test_chat_member = ChatMember(user=test_me, status=ChatMemberStatus.ADMINISTRATOR)


@patch.object(Bot, "get_chat_member", new_callable=lambda: test_chat_member)
@patch.object(Bot, "get_me", new_callable=lambda: test_me)
@patch.object(Bot, "close", new_callable=lambda: True)
@pytest.mark.asycncio
async def test_get_chat_member(close_bot, get_me, get_chat_member, fill_test_database):
    await check_bot_status()

    assert get_me.called_once()
    assert get_chat_member.call_args == (
        (),
        {"chat_id": "test_channel", "user_id": "test_me"}
    )
    assert close_bot.called_once()
