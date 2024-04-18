from aiogram.fsm.state import StatesGroup, State


class ProPlayer(StatesGroup):
    name = State()


class Hero(StatesGroup):
    name = State()
