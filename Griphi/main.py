import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import converter

from env.env_reader import get_token

async def main():
    bot = Bot(token=get_token())
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(converter.router)

    print("BOT --> WORKS")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    asyncio.run(main())