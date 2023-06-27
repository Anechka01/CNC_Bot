import asyncio
from aiogram import Bot, Dispatcher
from questions import router as r1
from different_types import router as r2

import os

# Запуск бота
async def main():
    bot = Bot(token="5915538782:AAE2ZER7pduQGDiKeAJyvPniUIKuUlO9KVM")
    dp = Dispatcher()

    dp.include_routers(r1, r2)

    # Альтернативный вариант регистрации роутеров по одному на строку
    # dp.include_router(questions.router)
    # dp.include_router(different_types.router)

    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())