
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import WebAppInfo
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup,  KeyboardButton, ReplyKeyboardMarkup, Message
from dotenv import load_dotenv
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import timedelta
from aiohttp import web
import aiohttp
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
ADMINS = [1805060245]  # Замените на ваш ID

@dp.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id not in ADMINS:
        return await message.answer("⛔ Доступ запрещён")
    
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="📊 Все бронирования",
            callback_data="admin_all_bookings"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🚗 Управление машинами",
            callback_data="admin_manage_cars"
        )
    )
    
    await message.answer(
        "🔐 Админ-панель:",
        reply_markup=builder.as_markup()
    )

@dp.callback_query(F.data == "admin_all_bookings")
async def show_all_bookings(callback: types.CallbackQuery):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "http://localhost:8000/admin/bookings",
                params={"user_id": callback.from_user.id}
            ) as resp:
                data = await resp.json()
                
        bookings_list = "\n".join(
            f"{b['model']} - {b['booking_date']} {b['booking_start_time']}"
            for b in data["bookings"]
        )
        await callback.message.edit_text(
            f"📋 Все бронирования:\n{bookings_list}",
            reply_markup=InlineKeyboardBuilder().button(
                text="Назад",
                callback_data="admin_back"
            ).as_markup()
        )
    except Exception as e:
        await callback.answer(f"Ошибка: {str(e)}", show_alert=True)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Открыть Mini App",
             web_app=WebAppInfo(url="https://auto-booking-bot.onrender.com")
        )]
    ])
    await message.answer("Добро пожаловать! Открой Mini App:", reply_markup=markup)

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())



















