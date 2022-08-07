from aiogram.utils.callback_data import CallbackData
from aiogram.types import ReplyKeyboardRemove, \
    InlineKeyboardMarkup, InlineKeyboardButton

data = CallbackData('en', 'ru')

button_en = InlineKeyboardButton('English', callback_data='en')
button_ru = InlineKeyboardButton('Русский', callback_data='ru')

greet_kb = InlineKeyboardMarkup(resize_keyboard=True).row(button_en, button_ru)