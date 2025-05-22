
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import WebAppInfo
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup,  KeyboardButton, ReplyKeyboardMarkup, Message
from dotenv import load_dotenv
from datetime import timedelta
from aiohttp import web
import os
import asyncio
from datetime import datetime
import json

routes = web.RouteTableDef()

# Загрузка токена из .env
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Список админов
ADMINS = [1805060245]

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Открыть Mini App",
            web_app=WebAppInfo(url="https://auto-school-bot-mkxv.onrender.com")
        )]
    ])
    await message.answer("Добро пожаловать! Открой Mini App:", reply_markup=markup)

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())



















