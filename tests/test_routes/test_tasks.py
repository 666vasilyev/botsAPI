from fastapi.testclient import TestClient
import pytest


@pytest.mark.asyncio
def test_get_task_by_id(mock_client: TestClient):
    task_id = "12345"
    response = mock_client.get(f"/task/{task_id}")
    assert response.status_code == 200
    task = response.json()
    assert task["task_id"] == task_id
    # Проверьте другие ожидаемые атрибуты задачи


@pytest.mark.asyncio
def test_get_tasks(mock_client: TestClient):
    response = mock_client.get("/task/")
    assert response.status_code == 200
    tasks = response.json()["tasks"]
    assert len(tasks) > 0
