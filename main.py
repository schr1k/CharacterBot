import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, WebAppData
from redis.asyncio import Redis

import amplitude
import gpt
import kb
from config import *
from states import *
from db import DB

db = DB()

redis = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB
)
storage = RedisStorage(redis)

bot = Bot(token=TOKEN, disable_web_page_preview=True)
dp = Dispatcher(storage=storage)

logging.basicConfig(filename="all.log", level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s function: %(funcName)s line: %(lineno)d - %(message)s')
errors = logging.getLogger("errors")
errors.setLevel(logging.ERROR)
fh = logging.FileHandler("errors.log")
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s function: %(funcName)s line: %(lineno)d - %(message)s')
fh.setFormatter(formatter)
errors.addHandler(fh)


@dp.message(Command('start'))
async def start(message: Message):
    try:
        if not await db.user_exists(str(message.from_user.id)):
            await amplitude.send_event(str(message.from_user.id), 'registration')
            await db.create_user(str(message.from_user.id), message.from_user.username,
                                 message.from_user.first_name, message.from_user.last_name,
                                 datetime.now())
            await message.answer('Приветствуем в боте Character Ai.\n'
                                 'Нажмите на кнопку чтобы сменить персонажа.', reply_markup=kb.main_kb)
        else:
            await message.answer('Нажмите на кнопку чтобы сменить персонажа.', reply_markup=kb.main_kb)
    except Exception as e:
        errors.error(e)


@dp.message(Command('menu'))
async def menu(message: Message):
    try:
        if not await db.user_exists(str(message.from_user.id)):
            await message.answer('Сначала пройдите регистрацию по команде /start.', reply_markup=kb.main_kb)
        else:
            await message.answer('Нажмите на кнопку чтобы сменить персонажа.', reply_markup=kb.main_kb)
    except Exception as e:
        errors.error(e)


@dp.message(F.web_app_data)
async def get_data(data: WebAppData, state: FSMContext):
    try:
        await amplitude.send_event(str(data.chat.id), 'change character')
        await db.change_character(str(data.chat.id), data.web_app_data.data)
        await bot.send_message(chat_id=data.chat.id,
                               text=await db.get_character_greeting(data.web_app_data.data),
                               reply_markup=None)
        await state.set_state(Chat.message)
    except Exception as e:
        errors.error(e)


@dp.message(Chat.message)
async def make_request(message: Message):
    try:
        await db.log_message(str(message.from_user.id), message.text)
        await amplitude.send_event(str(message.from_user.id), 'make request')
        user_character = await db.get_character(str(message.from_user.id))
        data = await gpt.make_request(await db.get_character_instruction(user_character), message.text)
        await amplitude.send_event(str(message.from_user.id), 'get response')
        await message.answer(data['choices'][0]['message']['content'])
        await db.log_message(str(message.from_user.id), data['choices'][0]['message']['content'])
        await amplitude.send_event(str(message.from_user.id), 'send answer')
    except Exception as e:
        errors.error(e)


async def main():
    await db.connect()
    await dp.start_polling(bot)


if __name__ == '__main__':
    print(f'Бот запущен ({datetime.now().strftime("%H:%M:%S %d.%m.%Y")}).')
    asyncio.run(main())
