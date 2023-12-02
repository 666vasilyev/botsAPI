from contextlib import ExitStack

import pytest_asyncio
from fastapi.testclient import TestClient

from src.app import get_app


@pytest_asyncio.fixture(scope="module", autouse=True)
def app():
    with ExitStack():
        yield get_app()


@pytest_asyncio.fixture(scope="module")
def mock_client(app):
    with TestClient(app) as c:
        yield c
