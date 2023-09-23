from src.utils import link_format
import pytest


@pytest.mark.asyncio
def test_link_format_with_https():
    assert link_format("https://t.me/telegramchannel") == "telegramchannel"


@pytest.mark.asyncio
def test_link_format_with_invalid_link():
    assert link_format("telegramchannel") == "telegramchannel"
