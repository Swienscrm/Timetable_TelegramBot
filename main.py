import logging
from config import BOT_TOKEN
from aiogram import Bot, Dispatcher
import asyncio
from handlers import router
from scheduler import setup_scheduler, scheduler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


if BOT_TOKEN is None:
    raise RuntimeError("BOT_TOKEN не установлен")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)

async def main():
    logging.info("Bot is running...")
    setup_scheduler(bot)
    try:
        await dp.start_polling(bot)
    finally:
        scheduler.shutdown()


if __name__ == "__main__":
    asyncio.run(main())