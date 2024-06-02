import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from env.env_reader import get_token

bot = Bot(token=get_token())

from handlers import converter

async def main():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(converter.router)
    print("STORAGE --> WORKS")

    await bot.delete_webhook(drop_pending_updates=True)
    print("BOT     --> WORKS")

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot was stopped by Ctrl-C")
