from aiogram.types import ReplyKeyboardRemove, \
    InlineKeyboardMarkup, InlineKeyboardButton

button_en = InlineKeyboardButton('English', callback_data='choose_en')
button_ru = InlineKeyboardButton('Русский', callback_data='choose_ru')

greet_kb = InlineKeyboardMarkup(resize_keyboard=True).row(button_en, button_ru)