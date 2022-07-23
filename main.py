from email import message
import logging
import time
import os

from aiogram import Bot, Dispatcher, executor, types # URLInputFile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urlextract import URLExtract
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


def makeScreen(url):
        options = webdriver.ChromeOptions()
        options.headless = True
        driver = webdriver.Chrome(options=options)

        driver.get(url)

        S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
        driver.set_window_size(S('Width'),S('Height')) # May need manual adjustment                                                                                                                
        screenshot = driver.find_element_by_tag_name('body').screenshot('web_screenshot.png')

        driver.quit()

        return screenshot


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    
    await message.reply(f"Hi, {message.from_user.first_name}!\nI'm Imager Telegram bot!")


@dp.message_handler()
async def echo(message: types.Message):

    extractorURL = URLExtract()
    url = extractorURL.find_urls(message.text)
    if url:
        makeScreen(url)
        await message.answer('Bee monster is activated!')
        await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp)