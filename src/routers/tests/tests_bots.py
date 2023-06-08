from unittest.mock import MagicMock
import pytest
from fastapi.testclient import TestClient

from main import app
from src.db.crud import (
    get_bot_by_id,
    add_bot,
    add_new_bundle,
    remove_channel_from_bot,
    add_channel_to_bot_by_bot_id,
    get_all_channels,
    get_bot_token_by_channel_id,
    get_bot_url_by_channel_id,
    get_bot_with_min_channels_count, get_all_bots
)
from src.models import BasicBotsModel

# client = TestClient(app)


@pytest.mark.asyncio
async def test_add_bot(mocker):
    bot_data = BasicBotsModel(
        alias="testbot",
        description="Test Bot",
        name="Test Bot",
        token="test_token",
        channels=[],
    )
    # Создаем асинхронные моки для сеанса и функции add_bot
    async with MagicMock() as session:
        mocker.patch("src.db.session.get_session", return_value=session)
        mocker.patch("src.db.crud.add_bot", side_effect=add_bot)

        # Вызываем функцию, которую тестируем
        bot_id = await add_bot(bot_data, session)

    # Проверяем результаты теста
    # None != None тест не проходит
    
    assert bot_id is not None
    # TODO: Дополнительные проверки, например:
    #   Проверить, что бот добавлен в базу данных
    #   Проверить, что данные бота соответствуют ожиданиям


#
# @pytest.mark.asyncio
# async def test_get_all_bots(mocker: MockFixture):
#     bot_data1 = {
#         "alias": "testbot1",
#         "description": "Test Bot 1",
#         "name": "Test Bot 1",
#         "token": "test_token1"
#     }
#     bot_data2 = {
#         "alias": "testbot2",
#         "description": "Test Bot 2",
#         "name": "Test Bot 2",
#         "token": "test_token2"
#     }
#     session = await get_session()
#     mocker.patch("src.routers.get_session", return_value=session)
#     mocker.patch("src.routers.get_all_bots", side_effect=get_all_bots)
#
#     # Добавляем боты в базу данных
#     await add_bot(bot_data1, session)
#     await add_bot(bot_data2, session)
#
#     all_bots = await get_all_bots(session)
#
#     assert len(all_bots) == 2
#     # TODO: Дополнительные проверки, например:
#     #   Проверить, что полученные данные ботов соответствуют ожиданиям
#     #   Проверить, что все боты получены из базы данных
#
#
# @pytest.mark.asyncio
# async def test_delete_bot(mocker: MockFixture):
#     bot_data = {
#         "alias": "testbot",
#         "description": "Test Bot",
#         "name": "Test Bot",
#         "token": "test_token"
#     }
#     session = await get_session()
#     mocker.patch("src.routers.get_session", return_value=session)
#     mocker.patch("src.routers.get_bot_by_id", side_effect=get_bot_by_id)
#
#     bot_id = await add_bot(bot_data, session)
#
#     response = client.delete(f"/bot/{bot_id}/")
#     assert response.status_code == 200
#     assert response.json()["status"] == "Success"
#
#     # Проверяем, что бот был удален
#     with pytest.raises(Exception):
#         await get_bot_by_id(bot_id, session)
#
#
# @pytest.mark.asyncio
# async def test_update_bot(mocker: MockFixture):
#     bot_data = {
#         "alias": "testbot",
#         "description": "Test Bot",
#         "name": "Test Bot",
#         "token": "test_token"
#     }
#     session = await get_session()
#     mocker.patch("src.routers.get_session", return_value=session)
#     mocker.patch("src.routers.get_bot_by_id", side_effect=get_bot_by_id)
#
#     bot_id = await add_bot(bot_data, session)
#
#     update_data = {
#         "alias": "updated_bot",
#         "description": "Updated Bot"
#     }
#
#     response = client.patch(f"/bot/{bot_id}/", json=update_data)
#     assert response.status_code == 200
#     assert response.json()["status"] == "Bot successfully updated"
#
#     # Получаем обновленные данные бота
#     updated_bot = await get_bot_by_id(bot_id, session)
#     assert updated_bot.alias == "updated_bot"
#     assert updated_bot.description == "Updated Bot"
#
#
# @pytest.mark.asyncio
# async def test_get_bot_by_id(mocker: MockFixture):
#     bot_data = {
#         "alias": "testbot",
#         "description": "Test Bot",
#         "name": "Test Bot",
#         "token": "test_token"
#     }
#     session = await get_session()
#     mocker.patch("src.routers.get_session", return_value=session)
#     mocker.patch("src.routers.get_bot_by_id", side_effect=get_bot_by_id)
#
#     bot_id = await add_bot(bot_data, session)
#
#     response = client.get(f"/bot/{bot_id}/")
#     assert response.status_code == 200
#     assert response.json()["alias"] == "testbot"
#     assert response.json()["description"] == "Test Bot"
#
#
# @pytest.mark.asyncio
# async def test_add_channel_to_bot_by_bot_id(mocker: MockFixture):
#     bot_data = {
#         "alias": "testbot",
#         "description": "Test Bot",
#         "name": "Test Bot",
#         "token": "test_token"
#     }
#     session = await get_session()
#     mocker.patch("src.routers.get_session", return_value=session)
#     mocker.patch("src.routers.get_bot_by_id", side_effect=get_bot_by_id)
#     mocker.patch("src.routers.add_new_bundle", side_effect=add_new_bundle)
#
#     bot_id = await add_bot(bot_data, session)
#
#     response = client.post(f"/bot/{bot_id}/channels/", json={"channel": "channel1"})
#     assert response.status_code == 200
#     assert response.json()["status"] == "Success"
#
#     # Проверяем, что канал добавлен к боту
#     bot = await get_bot_by_id(bot_id, session)
#     assert "channel1" in bot.channels
#
#
# @pytest.mark.asyncio
# async def test_remove_channel_from_bot(mocker: MockFixture):
#     bot_data = {
#         "alias": "testbot",
#         "description": "Test Bot",
#         "name": "Test Bot",
#         "token": "test_token"
#     }
#     session = await get_session()
#     mocker.patch("src.routers.get_session", return_value=session)
#     mocker.patch("src.routers.get_bot_by_id", side_effect=get_bot_by_id)
#     mocker.patch("src.routers.remove_channel_from_bot", side_effect=remove_channel_from_bot)
#
#     bot_id = await add_bot(bot_data, session)
#
#     # Добавляем канал к боту
#     await add_channel_to_bot_by_bot_id(bot_id, "channel1")
#
#     response = client.delete(f"/bot/{bot_id}/channels/channel1")
#     assert response.status_code == 200
#     assert response.json()["status"] == "Success"
#
#     # Проверяем, что канал удален из бота
#     bot = await get_bot_by_id(bot_id, session)
#     assert "channel1" not in bot.channels
#
#
# @pytest.mark.asyncio
# async def test_get_all_channels(mocker: MockFixture):
#     bot_data = {
#         "alias": "testbot",
#         "description": "Test Bot",
#         "name": "Test Bot",
#         "token": "test_token"
#     }
#     session = await get_session()
#     mocker.patch("src.routers.get_session", return_value=session)
#     mocker.patch("src.routers.get_all_channels", side_effect=get_all_channels)
#
#     bot_id = await add_bot(bot_data, session)
#
#     # Добавляем каналы к боту
#     await add_channel_to_bot_by_bot_id(bot_id, "channel1")
#     await add_channel_to_bot_by_bot_id(bot_id, "channel2")
#
#     response = client.get("/channels/")
#     assert response.status_code == 200
#     assert response.json() == {"channels": ["channel1", "channel2"]}
#
#
# @pytest.mark.asyncio
# async def test_get_bot_token_by_channel_id(mocker: MockFixture):
#     bot_data = {
#         "alias": "testbot",
#         "description": "Test Bot",
#         "name": "Test Bot",
#         "token": "test_token"
#     }
#     session = await get_session()
#     mocker.patch("src.routers.get_session", return_value=session)
#     mocker.patch("src.routers.get_bot_by_id", side_effect=get_bot_by_id)
#     mocker.patch(
#         "src.routers.get_bot_token_by_channel_id", side_effect=get_bot_token_by_channel_id
#     )
#
#     bot_id = await add_bot(bot_data, session)
#
#     # Добавляем канал к боту
#     await add_channel_to_bot_by_bot_id(bot_id, "channel1")
#
#     response = client.get("/channel/channel1/token")
#     assert response.status_code == 200
#     assert response.json() == {"bot_token": "test_token"}
#
#
# @pytest.mark.asyncio
# async def test_get_bot_url_by_channel_id(mocker: MockFixture):
#     bot_data = {
#         "alias": "testbot",
#         "description": "Test Bot",
#         "name": "Test Bot",
#         "token": "test_token"
#     }
#     session = await get_session()
#     mocker.patch("src.routers.get_session", return_value=session)
#     mocker.patch("src.routers.get_bot_by_id", side_effect=get_bot_by_id)
#     mocker.patch(
#         "src.routers.get_bot_url_by_channel_id", side_effect=get_bot_url_by_channel_id
#     )
#
#     bot_id = await add_bot(bot_data, session)
#
#     # Добавляем канал к боту
#     await add_channel_to_bot_by_bot_id(bot_id, "channel1")
#
#     response = client.get("/channel/channel1/url")
#     assert response.status_code == 200
#     assert response.json() == {"alias": "testbot"}
#
#
# @pytest.mark.asyncio
# async def test_get_bot_with_min_channels_count(mocker: MockFixture):
#     bot_data1 = {
#         "alias": "testbot1",
#         "description": "Test Bot 1",
#         "name": "Test Bot 1",
#         "token": "test_token1"
#     }
#     bot_data2 = {
#         "alias": "testbot2",
#         "description": "Test Bot 2",
#         "name": "Test Bot 2",
#         "token": "test_token2"
#     }
#     session = await get_session()
#     mocker.patch("src.routers.get_session", return_value=session)
#     mocker.patch("src.routers.get_bot_by_id", side_effect=get_bot_by_id)
#     mocker.patch(
#         "src.routers.get_bot_with_min_channels_count", side_effect=get_bot_with_min_channels_count
#     )
#
#     # Добавляем боты с разным количеством каналов
#     bot_id1 = await add_bot(bot_data1, session)
#     bot_id2 = await add_bot(bot_data2, session)
#
#     # Добавляем каналы к ботам
#     await add_channel_to_bot_by_bot_id(bot_id1, "channel1")
#     await add_channel_to_bot_by_bot_id(bot_id1, "channel2")
#     await add_channel_to_bot_by_bot_id(bot_id2, "channel1")
#
#     response = client.get("/bot/min_channels_count")
#     assert response.status_code == 200
#     assert response.json() == {
#         "id": bot_id2,
#         "alias": "testbot2",
#         "description": "Test Bot 2",
#         "name": "Test Bot 2",
#         "token": "test_token2",
#         "channels": ["channel1"]
#     }
