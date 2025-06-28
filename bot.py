from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import logging
import os

# 🔐 Получаем токен из переменной окружения
API_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_USERNAME = '@RusanovMentor'

if not API_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Создаем клавиатуру с постоянным отображением
main_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=False,  # Кнопка остается после нажатия
    input_field_placeholder="Нажмите кнопку ниже 👇"  # Скрывает строку ввода
)
main_keyboard.add(KeyboardButton("📖 Получить гайд"))

async def check_subscription_and_send_guide(message: types.Message):
    """Функция для проверки подписки и отправки гайда"""
    user_id = message.from_user.id
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ['creator', 'administrator', 'member']:
            await message.answer(
                "✅ Спасибо, что подписались на канал!\n\n"
                "📚 Ваш гайд: https://teletype.in/@andrusanov/2PeMdy1IRJh",
                reply_markup=main_keyboard
            )
        else:
            raise Exception("Not subscribed")
    except:
        await message.answer(
            "❌ Для получения гайда нужно подписаться на канал: https://t.me/RusanovMentor",
            reply_markup=main_keyboard
        )

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(
        "Привет! Нажми кнопку ниже или введи /start, чтобы получить гайд\n"
        "Важно: ты должен быть подписан на канал 👉 https://t.me/RusanovMentor",
        reply_markup=main_keyboard
    )
    # Автоматически проверяем подписку и отправляем гайд
    await check_subscription_and_send_guide(message)

@dp.message_handler(text="📖 Получить гайд")
async def send_guide(message: types.Message):
    await check_subscription_and_send_guide(message)

# Обработчик для всех остальных сообщений
@dp.message_handler()
async def handle_other_messages(message: types.Message):
    await message.answer(
        "Используйте кнопку ниже для получения гайда 👇",
        reply_markup=main_keyboard
    )

if __name__ == '__main__':
    executor.start_polling(dp)
