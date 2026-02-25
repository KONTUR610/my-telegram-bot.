import asyncio
import logging
from datetime import datetime
import pytz
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message

# ВСТАВТЕ ВАШ ТОКЕН ТУТ
API_TOKEN = '8605231816:AAGMpIZHdtEcmMDXUT1CA9wfN7AaVv1WbQ0'
UKRAINE_TZ = pytz.timezone('Europe/Kyiv')

# Ваш особистий ID (щоб бот не забував вас після перезавантаження)
USER_ID = 1018336332 

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def morning_reminder():
    while True:
        now = datetime.now(UKRAINE_TZ)
        # Перевірка: 9:00 ранку, Понеділок-П'ятниця (weekday < 5)
        if now.hour == 9 and now.minute == 0 and now.weekday() < 5:
            if USER_ID:
                try:
                    await bot.send_message(USER_ID, "⏰ Доброго ранку! Пора подзвонити адвокату.")
                    logging.info("Повідомлення надіслано.")
                except Exception as e:
                    logging.error(f"Помилка відправки: {e}")
            
            # Чекаємо 61 секунду, щоб не було повторів у ту ж хвилину
            await asyncio.sleep(61)
        
        # Перевірка кожні 30 секунд
        await asyncio.sleep(30)

@dp.message(CommandStart())
async def cmd_start(message: Message):
    global USER_ID
    USER_ID = message.from_user.id
    await message.answer(f"✅ Бот активований! Ваш ID {USER_ID} збережено. Нагадування на 09:00 працює.")

async def main():
    # Запускаємо таймер
    asyncio.create_task(morning_reminder())
    # Запускаємо бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот вимкнений")
