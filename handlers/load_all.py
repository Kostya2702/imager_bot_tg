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

print(dp.loop)
db = dp.loop.run_until_complete(create_pool())