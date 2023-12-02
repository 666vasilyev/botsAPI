from fastapi.testclient import TestClient
import pytest

from src.models import MessagesPostResModel


@pytest.mark.asyncio
def test_post_messages(mock_client: TestClient):
    posted_message = MessagesPostResModel(channel_id='test_channel', message='test message')
    response = mock_client.post("/message", data=posted_message.json())
    assert response.status_code == 200
    # task_id = response.json()["task_id"]

    # Проверяем, что в ответе есть поле "task_id"
    # assert "task_id" in response.json()

