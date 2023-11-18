from aiogram.fsm.state import State, StatesGroup


class Chat(StatesGroup):
    message = State()
