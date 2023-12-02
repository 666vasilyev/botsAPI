import pytest
from fastapi.testclient import TestClient

from src.routers.bots.models import BotCreate, BotUpdate


@pytest.mark.asyncio
async def test_get_bots_empty(mock_client: TestClient):
    bots = [
        BotCreate(
            bot_token="first",
            name="first",
            alias="first_bot",
            description="first_bot"
        ),
        BotCreate(
            bot_token="second",
            name="second",
            alias="second_bot",
            description="second_bot",
        ),
    ]

    for bot in bots:
        response = mock_client.post("/bot", data=bot.json())
        assert response.status_code == 200

    response = mock_client.get("/bot").json()

    assert [BotCreate.parse_obj(bot) for bot in response] == bots

    for bot in response:
        mock_client.delete(f"/{bot['id']}")


@pytest.mark.asyncio
async def test_post_bot(mock_client: TestClient):
    bot = BotCreate(
        bot_token="test_123",
        name="test_123",
        alias="test_123",
        description="test_123"
    )
    response = mock_client.post("/bot", data=bot.json())
    assert "id" in response.json()


@pytest.mark.asyncio
async def test_delete_bot(mock_client: TestClient):
    bot_data = BotCreate(
        bot_token="test_token",
        name="Test Bot",
        alias="testbot",
        description="Test Bot"
    )

    # Создаем бота для тестирования
    response = mock_client.post("/bot", data=bot_data.json())
    assert response.status_code == 200

    bot_id = response.json()["id"]

    # Удаляем бота
    response = mock_client.delete(f"/bot/{bot_id}")
    assert response.status_code == 200

    # Проверяем, что бот был успешно удален из базы данных
    # Например, с помощью запроса GET или других функций проверки базы данных

    # Пытаемся получить информацию об удаленном боте (должно вернуть ошибку)
    response = mock_client.get(f"/bot/{bot_id}")
    assert response.status_code == 404


# TODO: ValueError: too many values to unpack (expected 2)
@pytest.mark.asyncio
async def test_update_bot(mock_client: TestClient):
    # Создаем бота для тестирования
    bot_data = BotCreate(
        bot_token="test_token6",
        name="Test Bot6",
        alias="testbot6",
        description="Test Bot6"
    )
    response = mock_client.post("/bot", data=bot_data.json())
    assert response.status_code == 200

    bot_id = response.json()["id"]

    # Новые данные для обновления бота
    updated_data = BotUpdate(
        bot_token="test_token3",
        name="Test Bot3",
        alias="Updated_testbot3",
        description="Updated Bot3"
    )

    # Обновляем данные бота
    response = mock_client.patch(f"/bot/{bot_id}", data=updated_data.json())
    assert response.status_code == 200

    # # Проверяем, что данные бота были успешно обновлены
    # response = mock_client.get(f"/bot/{bot_id}")
    # assert response.status_code == 200
    # response = mock_client.get("/bot").json()
    # assert BotCreate.parse_obj(updated_data) == response
