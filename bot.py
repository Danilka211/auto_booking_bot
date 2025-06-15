
import logging
import os
import asyncio
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup, Message, BotCommandScopeChat
from aiogram.filters import Command, StateFilter

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "1234")

# ID админов
ADMINS = [1805060245]  # Замени на свой Telegram ID

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Состояние для ввода пароля
class AdminAuth(StatesGroup):
    waiting_for_password = State()

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Открыть Mini App",
            web_app=WebAppInfo(url="https://auto-booking-bot.onrender.com")
        )]
    ])
    await message.answer("Добро пожаловать! Открой Mini App:", reply_markup=markup)

# Команда /admin
@dp.message(Command("admin"))
async def admin_command(message: types.Message, state: FSMContext):
    if message.from_user.id not in ADMINS:
        await message.answer("❌ У вас нет доступа к админке.")
        return
    await message.answer("🔐 Введите пароль для входа в админку:")
    await state.set_state(AdminAuth.waiting_for_password)

@dp.message(StateFilter(AdminAuth.waiting_for_password), F.text)
async def check_admin_password(message: Message, state: FSMContext):
    if message.text == ADMIN_PASSWORD:
        await state.clear()
        await message.answer(
            '✅ Пароль верный.\n'
            '<a href="https://auto-booking-bot.onrender.com/admin">Открыть админку</a>',
            parse_mode="HTML"
        )
    else:
        await message.answer("❌ Неверный пароль. Попробуйте ещё раз:")


# Установка команды /admin только для админа
@dp.startup()
async def on_startup(bot: Bot):
    await bot.set_my_commands(
        [types.BotCommand(command="admin", description="Вход в админку")],
        scope=BotCommandScopeChat(chat_id=ADMINS[0])
    )

# Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
















