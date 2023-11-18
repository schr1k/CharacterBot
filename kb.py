from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, ReplyKeyboardMarkup, WebAppInfo

web_app = WebAppInfo(url='https://schr1k.github.io/CharacterWebApp/')
choose_character = KeyboardButton(text='Выбрать персонажа.', web_app=web_app)
main_kb = ReplyKeyboardMarkup(keyboard=[[choose_character]], resize_keyboard=True, one_time_keyboard=True)
