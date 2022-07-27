from datetime import datetime
import imp
import logging
import re
import os

from requests import get
from aiogram import Bot, Dispatcher, executor, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from selenium import webdriver
from urlextract import URLExtract
from dotenv import load_dotenv

load_dotenv()

# Bot parameters
TOKEN = os.getenv('TOKEN')
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
scheduler = AsyncIOScheduler()
scheduler.start()

async def make_screen(url):

    # Initialize Chrome webrdiver
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    driver.get(url)

    # Setting up display size
    required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    driver.set_window_size(required_width, required_height)
    driver.maximize_window()

    # Makes screenshot
    driver.get_screenshot_as_file('web_screenshot.png')

    # Ending driver work
    driver.quit()


# Bot functionality description function
@dp.message_handler(commands=['start', 'help'], content_types=types.ContentTypes.ANY)
async def send_welcome(message: types.Message):

    # Answer on message about bot
    await message.reply(f"Hi, {message.from_user.first_name}!\nI'm Imager Telegram bot!")


# Photo creation, URL extraction and request time
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def send_screen(message: types.Message):

    # Getting url from message
    extractorURL = URLExtract()
    url = extractorURL.find_urls(message.text)
    full_url = []
    
    if url:
        full_url = re.findall('^http.*', url[0])
    else:
        await message.answer('Сообщение должно содержать URL сайта')
        return
        
    # Transfromation url to https request
    if len(full_url) == 0:
        full_url.append(f"https://{url[0]}")

    # Getting page title from url
    headers = get(full_url[0])
    page_title = re.findall(r'<title>(.*?)</title>', headers.text)[0]
    
    # Makes photo and add job for scheluder for edit_message handler
    if full_url:

        message = await message.reply('🐝 Bee monster is activated!\n🪄 Ваш запрос выполняется')
        
        starting_capture_screen = datetime.now().second
        await make_screen(full_url[0])
        time_request = datetime.now().second - starting_capture_screen

        scheduler.add_job(edit_message, 
                          "date",
                          run_date=datetime.now(), 
                          kwargs={"message": message, "page_title": page_title, "time_request": time_request})
                          

async def edit_message(message: types.Message, page_title, time_request):

    # Getting chat id
    chat_id = message.chat.id

    # Sending edited text with all necessary parameters
    # with open(f"{ROOT_DIR}/web_screenshot.png", 'rb') as forw_photo:
    reply_photo = await bot.send_photo(chat_id, open(f"{ROOT_DIR}/web_screenshot.png", 'rb'))
    await message.edit_media(f"{page_title}\n{time_request}\n{reply_photo}")


if __name__ == '__main__':
    executor.start_polling(dp)