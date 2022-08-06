import pytest

from unittest.mock import AsyncMock
from main import send_welcome


@pytest.mark.asyncio
async def test_echo_handler():
    text_mock = "test123"
    message_mock = AsyncMock(text=text_mock)
    await send_welcome(message=message_mock)
    message_mock.answer.assert_called_with(text_mock)
