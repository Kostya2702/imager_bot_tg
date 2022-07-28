from datetime import date, datetime
import logging
import re
import os
from urllib.parse import urlparse

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

def filter_python(record: logging.LogRecord) -> bool:
    return record.getMessage().find('aiogram') != -1

# logging.basicConfig(level=logging.DEBUG)

# create logger
logger = logging.getLogger('debug information')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
d_handler = logging.FileHandler(filename='debug_logs.log')
d_handler.setLevel(logging.DEBUG)

# create console handler with a higher log level
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.ERROR)

# create formatter and add it to the handlers
formatter = logging.Formatter('[%(asctime)s: %(name)s - %(levelname)s] %(message)s')
d_handler.setFormatter(formatter)
c_handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(d_handler)
logger.addHandler(c_handler)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
scheduler = AsyncIOScheduler()
scheduler.start()

async def make_screen(url, date_request, user_id, domen):

    # Initialize Chrome webrdiver
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
    except Exception:
        logger.exception('InvalidArgumentException')

    # Setting up display size
    driver.set_window_size(1024, 1460)
    driver.maximize_window()

    # Makes screenshot
    driver.get_screenshot_as_file(f"{date_request}_{user_id}_{domen}.png")

    # Ending driver work
    driver.quit()


# Bot functionality description function
@dp.message_handler(commands=['start', 'help'], content_types=types.ContentTypes.ANY)
async def send_welcome(message: types.Message):

    # Answer on message about bot
    with open(f"{ROOT_DIR}/greetings.txt", 'r', encoding='UTF-8') as greeting:
        await message.answer(greeting.read())
        logger.info(f"Sending gretting for user {message.from_user.first_name}")


# Photo creation, URL extraction and request time
@dp.message_handler(content_types=types.ContentTypes.ANY)
async def send_screen(message: types.Message):

    logger.info(f"Starting work with user: {message.from_user.first_name}")

    # Getting url from message
    extractorURL = URLExtract()
    url = extractorURL.find_urls(message.text)
    full_url = []
    
    if url:
        full_url = re.findall('^http.*', url[0])
        logger.info('Finding request method to url')
    else:
        await message.answer('Сообщение должно содержать URL сайта')
        return
        
    # Transfromation url to https request
    if len(full_url) == 0:
        full_url.append(f"https://{url[0]}")
        logger.info('Adding request method to url')

    # Getting page title from url
    headers = get(full_url[0])
    page_title = re.findall(r'<title>[\n\t\s]*(.*?)[\n\t\s]*<\/title>', headers.text)[0]
    logger.info('Find page title is complete')

    # Getting site domain
    page_domain = urlparse(full_url[0]).netloc

    # Makes photo and add job for scheluder for edit_message handler
    if full_url:
        
        message = await message.reply('🪄 Ваш запрос выполняется')
        logger.info('Sending dummy message')
        
        starting_capture_screen = datetime.now().second
        logger.info('Starting a screenshot')
        
        try:
            await make_screen(full_url[0],
                            date.today(),
                            message.from_user.id, page_domain)
        except Exception:
            logger.exception('Exception occurred')

        logger.info('Ending a screenshot')
        time_request = datetime.now().second - starting_capture_screen

        logger.info('Creating a job for the scheduler')
        scheduler.add_job(edit_message, 
                          "date",
                          run_date=datetime.now(),
                          kwargs={"message": message,
                                  "page_title": page_title,
                                  "time_request": time_request,
                                  "page_domain": page_domain})
                          

async def edit_message(message: types.Message, page_title, time_request, page_domain):

    plural_name = ''

    if str(time_request)[-1] == '1':
        plural_name = 'секунда'
    if str(time_request)[-1] in ['2', '3', '4']:
        plural_name = 'секунды'
    if str(time_request)[-1] not in ['1', '2', '3', '4']:
        plural_name = 'секунд'
        
    # Sending edited text with all necessary parameters
    logger.info('Running the scheduler')
    with open(f"{ROOT_DIR}/{date.today()}_{message.from_user.id}_{page_domain}.png", 'rb') as forw_photo:
        await message.delete()
        logger.info('Editing dummy message and sending answer with photo and captions')
        await message.answer_photo(photo=forw_photo, 
                                   caption=f"{page_title}\n\nВремя обработки: {time_request} {plural_name}")


if __name__ == '__main__':
    executor.start_polling(dp)
    logger.info('Ending a bot work')