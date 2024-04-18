from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram import Router

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    choose_kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [
            KeyboardButton(text='Pro Players'),
            KeyboardButton(text='Heroes'),
            KeyboardButton(text='Meta')
        ]
    ])
    await message.answer('Choose category', reply_markup=choose_kb)
