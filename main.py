import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from requests import request

load_dotenv()

TOKEN = os.getenv('TOKEN')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(f"Hi, {message.from_user}!\nI'm Imager Telegram bot!")


@dp.message_handler()
async def echo(message: types.Message):

    # All text messages handler
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)