import pytest
import sys
import os
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
print(Path(__file__))

sys.path.insert(1, f"{Path(__file__).parent.parent}/handlers")

from unittest.mock import AsyncMock
from main import send_welcome, get_stats


@pytest.mark.asyncio
async def test_echo_handler():
    text_mock = "test123"
    message_mock = AsyncMock(text=text_mock)
    await send_welcome(message=message_mock)
    message_mock.answer.assert_called_with(text_mock)

@pytest.mark.asyncio
async def test_echo_handler():
    text_mock = "test123"
    message_mock = AsyncMock(text=text_mock)
    await get_stats(message=message_mock)
    message_mock.answer.assert_called_with(text_mock)
