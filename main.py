from datetime import datetime
import logging
import re
import os
import requests

from aiogram import Bot, Dispatcher, executor, types # URLInputFile
from selenium import webdriver
from urlextract import URLExtract
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
print(ROOT_DIR)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


async def make_screen(url):
        options = webdriver.ChromeOptions()
        options.headless = True
        driver = webdriver.Chrome(options=options)

        driver.get(url)

        required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
        required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        driver.set_window_size(required_width, required_height)
        driver.maximize_window()
        driver.get_screenshot_as_file('web_screenshot.png')

        driver.quit()


@dp.message_handler(commands=['start', 'help'], content_types=types.ContentTypes.ANY)
async def send_welcome(message: types.Message):

    await message.reply(f"Hi, {message.from_user.first_name}!\nI'm Imager Telegram bot!")


@dp.message_handler(content_types=types.ContentTypes.ANY)
async def send_screen(message: types.Message):

    extractorURL = URLExtract()
    url = extractorURL.find_urls(message.text)[0]
    new_url = re.findall('^http.*', url)

    if len(new_url) == 0:
        new_url.append(f"https://{url}")

    headers = requests.get(new_url[0])
    title_page = re.findall(r'<title>(.*?)</title>', headers.text)[0]

    chat_id = message.chat.id
    
    if new_url:
        await message.reply('Bee monster is activated!\n🪄 Ваш запрос выполняется')
        await make_screen(new_url[0])
        with open(f"{ROOT_DIR}/web_screenshot.png", 'rb') as forw_photo:
            await bot.send_photo(chat_id, forw_photo)


if __name__ == '__main__':
    executor.start_polling(dp)