# import asyncio
import os

import asyncio
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from handlers.config import TOKEN
from handlers.db_definition import create_pool

# Set up storage
storage = MemoryStorage()

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)

new_loop = asyncio.new_event_loop()
asyncio.set_event_loop(new_loop)
db = new_loop.run_until_complete(create_pool())
ROOT_DIR = '/home/kostya/imager_bot_tg'

I18N_DOMAIN = 'imager_tg_bot'
LOCALES_DIR = f"{ROOT_DIR}/locales"

# Setup i18n middleware
i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR)
dp.middleware.setup(i18n)
# Alias for gettext method
_i = i18n.gettext