import re

from urllib.parse import urlparse
from requests import get
from aiogram import executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import date, datetime
from urlextract import URLExtract
from logger import logger
from sending_screen import make_screen
from load_all import bot, dp, ROOT_DIR
from config import ADMIN
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from Stats import Stats
from inlineButton import greet_kb


# Bot parameters
db = Stats()
I18N_DOMAIN = 'imager_tg_bot'
LOCALES_DIR = f"{ROOT_DIR}/locales"

# Initialize bot and dispatcher
scheduler = AsyncIOScheduler()
scheduler.start()

# Setup i18n middleware
i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR)
dp.middleware.setup(i18n)

# Alias for gettext method
_ = i18n.gettext


# States
class Form(StatesGroup):

    # State for choose language
    language = State()


async def set_default_commands():

    await bot.set_my_commands(
        [
            types.BotCommand('start', _("Starting bot"),
            types.BotCommand('statistic', _("Statistic")))
        ]
    )


@dp.message_handler(commands=['start'], content_types=['text'], state='*')
async def send_welcome(message: types.Message):

    # await Form.language.set()

    # Register user
    user = message.from_user
    await db.record_etries(user)

    # Answer on message about bot
    with open(f"{ROOT_DIR}/greetings.txt", 'r', encoding='UTF-8') as greeting:
        await message.answer(greeting.read())
        # await message.answer('f', reply_markup=button.greet_kb)
        logger.info(f"Sending gretting for user {message.from_user.first_name}")


@dp.message_handler(commands=['statistic'])
async def get_stats(message: types.Message):

    count_users = await db.count_users()
    await db.stats(count_users)
    count_users_today = await db.get_stats()
    
    if message.from_user.id == int(ADMIN):
        await message.answer(_("Total users in database: {users}\n"
                            "Used the bot today: {users_today}")
                                .format(users = count_users,
                                        users_today = count_users_today))
    else:
        await message.answer(_("You must be an administrator"))


# Photo creation, URL extraction and request time
@dp.message_handler(content_types=types.ContentTypes.ANY)
async def send_screen(message: types.Message):


    print(message.location)
    print(message.from_user.language_code)

    logger.info(f"Starting work with user: {message.from_user.first_name}")

    # await state.update_data(lang='ru')
    # await Form.next()
    # print(await state.get_data()['lang'])

    # Getting url from message
    extractorURL = URLExtract()
    url = extractorURL.find_urls(message.text)
    full_url = []
    
    if url:
        full_url = re.findall('^http.*', url[0])
        logger.info('Finding request method to url')
    else:
        await message.answer(_("Message must contain website URL"))
        logger.warning("Can't find URL in request")
        return
        
    # Transfromation url to https request
    if len(full_url) == 0:
        full_url.append(f"https://{url[0]}")
        logger.info('Adding request method to url')

    # Getting page title from url
    headers = get(full_url[0])
    page_title = re.findall(r'<title>[\n\t\s]*(.*?)[\n\t\s]*<\/title>', 
                            headers.text)[0]
    logger.info('Find page title is complete')

    # Getting site domain
    page_domain = urlparse(full_url[0]).netloc

    # Makes photo and add job for scheluder for edit_message handler
    if full_url:
        
        message = await message.reply(_("🪄 Your request is being processed"))
        logger.info('Sending dummy message')
        
        starting_capture_screen = datetime.now()
        logger.info('Starting a screenshot')
        
        try:
            await make_screen(full_url[0],
                            date.today(),
                            message.from_user.id, page_domain)
        except Exception:
            logger.exception('Exception occurred')

        logger.info('Ending a screenshot')
        time_request = datetime.now() - starting_capture_screen

        logger.info('Creating a job for the scheduler')
        scheduler.add_job(edit_message, 
                          "date",
                          run_date=datetime.now(),
                          kwargs={"message": message,
                                  "page_title": page_title,
                                  "time_request": time_request.seconds,
                                  "page_domain": page_domain})

    
                          

async def edit_message(message: types.Message, 
                       page_title, 
                       time_request, 
                       page_domain):

    plural_name = ''

    if str(time_request)[-1] == '1':
        plural_name = _("second")
    if str(time_request)[-1] in ['2', '3', '4']:
        plural_name = _("seconds")
    if str(time_request)[-1] not in ['1', '2', '3', '4']:
        plural_name = _("seconds")

    # Getting user id

    user_id = message.from_user.id
        
    # Sending edited text with all necessary parameters
    logger.info('Running the scheduler')
    try:
        with open(("{ROOT_DIR}/{date}_"\
                    "{user_id}_"\
                    "{page_domain}.png").format(ROOT_DIR=ROOT_DIR,
                                                date=date.today(),
                                                user_id=user_id,
                                                page_domain=page_domain), 'rb') as forw_photo:

            await message.delete()
            logger.info('Editing dummy message and sending answer with photo and captions')
            await message.answer_photo(forw_photo,
                                       _("{page_title}\n\nProcessing time: "\
                                        "{time_request} "\
                                        "{plural_name}").format(page_title=page_title,
                                                               time_request=time_request,
                                                               plural_name=plural_name))
    except FileNotFoundError:
        logger.exception('FileNotFoundError')


if __name__ == '__main__':
    executor.start_polling(dp)
    logger.info('Ending a bot work')