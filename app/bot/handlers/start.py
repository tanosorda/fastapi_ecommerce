from aiogram import Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

async def cmd_start(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('📦 Каталог'))
    await message.answer('Добро пожаловать! Выберите действие:', reply_markup=kb)


def register(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'])