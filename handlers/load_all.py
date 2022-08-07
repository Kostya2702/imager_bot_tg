from pathlib import Path

import asyncio
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN
from db_definition import create_pool

# Set up storage
storage = MemoryStorage()

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)

new_loop = asyncio.new_event_loop()
asyncio.set_event_loop(new_loop)
db = new_loop.run_until_complete(create_pool())
ROOT_DIR = Path(__file__).parent.parent