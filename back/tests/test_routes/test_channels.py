import pytest
from fastapi.testclient import TestClient
from src.models import ChannelPostResModelByBotId, ChannelPostResModel
from src.routers.bots.models import BotCreate


@pytest.mark.asyncio
async def test_get_channels_empty(mock_client: TestClient):
    # Очистить базу данных перед тестом
    # ...

    # Отправить GET-запрос на /channels
    response = mock_client.get("/channel")

    # Проверить код ответа
    assert response.status_code == 200

    # Проверить, что список каналов пустой
    assert response.json()['all_bundles'] == []


@pytest.mark.asyncio
async def test_post_channels(mock_client: TestClient):
    # Создать тестовый канал в базе данных
    channel_id = "test_channel_id"

    # Запостить канал, привязанный к любому bot_id
    channel = ChannelPostResModelByBotId(channel=channel_id)
    response = mock_client.post("/channel", data=channel.json())
    assert response.status_code == 200
    # TODO: Ответом будет ChannelPostReqModel, неплохо было бы обработать это, а не проверять только status_code


@pytest.mark.asyncio
async def test_post_channels_without_bot_id(mock_client: TestClient):
    # Отправить POST-запрос на /channels без указания bot_id
    channel = ChannelPostResModel(channel='test_channel_123')
    response = mock_client.post("/channel", data=channel.json())
    # Проверить код ответа
    assert response.status_code == 200

    # Проверить, что возвращается модель ChannelPostReqModel
    assert "channel_id" in response.json()
    assert "bot_link" in response.json()
    assert "message" in response.json()


@pytest.mark.asyncio
async def test_post_channels_with_bot_id(mock_client: TestClient):
    # Создать тестовый канал и связанный с ним бот в базе данных
    # Для этого создадим нового бота, заберем у него bot_id и запостим channel
    bot = BotCreate(
        bot_token="test_1234",
        name="test_1234",
        alias="test_1234",
        description="test_1234"
    )
    response = mock_client.post("/bot", data=bot.json())
    bot_id = response.json()['id']
    channel = ChannelPostResModelByBotId(channel='test_channel', bot_id=bot_id)
    response = mock_client.post("/channel", data=channel.json())
    # Проверить код ответа
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_channels_by_id(mock_client: TestClient):

    channel = 'test_channel'
    response = mock_client.get(f"/channel/{channel}")
    # Проверить код ответа
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_channels(mock_client: TestClient):
    def test_delete_channels():
        # Создаем тестовые данные
        bot_id = 1
        data = {
            "channel": "channel_name"
        }

        # Отправляем DELETE-запрос на /{bot_id}
        response = mock_client.delete(f"/{bot_id}", json=data)

        # Проверяем статус код
        assert response.status_code == 404
