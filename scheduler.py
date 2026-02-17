from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram import Bot
from schedule_service import generate_timetable_message
from config import GROUP_CHAT_ID, SCHEDULE_TIME
import logging

scheduler = AsyncIOScheduler()

async def send_timetable_to_group(bot: Bot):
    try:
        if GROUP_CHAT_ID is None:
            logging.warning("id чата не установлен")
            return

        message = generate_timetable_message()
        await bot.send_message(chat_id=GROUP_CHAT_ID, text=message)
        logging.info("Расписание отправлено в чат")
    except Exception as e:
        logging.error(f"Ошибка при отправке расписания {e}")

def setup_scheduler(bot:Bot):
    if not SCHEDULE_TIME or len(SCHEDULE_TIME.split())!=5:
        logging.error("SCHEDULE_TIME имеет неверный формат")
        return
    scheduler.add_job(
        send_timetable_to_group,
        trigger=CronTrigger.from_crontab(SCHEDULE_TIME),
        args=[bot],
        id="send_timetable",
        replace_existing=True,
        timezone="Asia/Novosibirsk"
    )
    logging.info("Планировщик настроен")
    scheduler.start()
    
