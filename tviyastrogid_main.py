import asyncio
import logging
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tviyastrogid_handlers import router, daily_broadcast
from config import BOT_TOKEN  # ✅ беремо токен з коду, не з env

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(router)

    # Київська таймзона для розсилки
    scheduler = AsyncIOScheduler(timezone="Europe/Kyiv")
    scheduler.add_job(daily_broadcast, "cron", hour=9, minute=0, args=[bot])
    scheduler.start()

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
