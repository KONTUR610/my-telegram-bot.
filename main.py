import asyncio
import logging
from datetime import datetime
import pytz
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message


# ВАШ ТОКЕН (той, що ви отримали від BotFather)
API_TOKEN = '8605231816:AAGMpIZHdtEcmMDXUT1CA9wfN7AaVv1WbQ0'


# Налаштування часового поясу України
UKRAINE_TZ = pytz.timezone('Europe/Kyiv')


# Ініціалізація бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


# Глобальна змінна для вашого ID (щоб бот знав, кому писати)
USER_ID = None 


# --- ФУНКЦІЯ НАГАДУВАННЯ (CLOUD LOGIC) ---
async def morning_reminder():
    global USER_ID
    while True:
        # Отримуємо час саме за Києвом
        now = datetime.now(UKRAINE_TZ)
        
        # Якщо зараз 09:00:00 (або перші секунди хвилини)
        if now.hour == 9 and now.minute == 0:
            if USER_ID:
                try:
                    await bot.send_message(USER_ID, "⏰ Доброго ранку! Нагадую: пора подзвонити адвокату.")
                    logging.info("Нагадування успішно надіслано.")
                except Exception as e:
                    logging.error(f"Помилка надсилання: {e}")
            
            # Чекаємо хвилину, щоб не слати повідомлення повторно в ту ж хвилину
            await asyncio.sleep(61)
        else:
            # Перевіряємо час кожні 30 секунд
            await asyncio.sleep(30)


# --- ОБРОБНИКИ ПОВІДОМЛЕНЬ ---
@dp.message(CommandStart())
async def cmd_start(message: Message):
    global USER_ID
    USER_ID = message.from_user.id # Бот запам'ятовує ваш ID
    await message.answer(
        "👋 Вітаю! Я ваш персональний Cloud Bot.\n\n"
        "✅ Я активував режим очікування: щоранку о 09:00 я буду писати вам про дзвінок адвокату."
    )


@dp.message()
async def echo_all(message: Message):
    # Підтвердження, що бот працює
    await message.answer(f"Ви написали: '{message.text}'. Нагадування на 09:00 активне!")


# --- ЗАПУСК ---
async def main():
    # Запускаємо таймер нагадування у фоновому режимі
    asyncio.create_task(morning_reminder())
    # Починаємо слухати повідомлення
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот зупинений.")