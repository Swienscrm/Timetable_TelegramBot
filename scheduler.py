from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram import Bot
from schedule_service import generate_timetable_message, get_today_assignment
from config import GROUP_CHAT_ID, SCHEDULE_TIME_WEEK, SCHEDULE_TIME_EVERY_DAY
import logging

scheduler = AsyncIOScheduler()

#EVERY WEEK
async def send_timetable_to_group(bot: Bot):
    try:
        if GROUP_CHAT_ID is None:
            logging.warning("id чата не установлен")
            return

        message = generate_timetable_message()
        await bot.send_message(chat_id=GROUP_CHAT_ID, text=message)
        logging.info("Еженедельное расписание отправлено в чат")
    except Exception as e:
        logging.error(f"Ошибка при отправке расписания {e}")

def setup_scheduler(bot: Bot):
    if not SCHEDULE_TIME_WEEK or len(SCHEDULE_TIME_WEEK.split())!=5:
        logging.error("SCHEDULE_TIME_WEEK имеет неверный формат")
        return
    scheduler.add_job(
        send_timetable_to_group,
        trigger=CronTrigger.from_crontab(SCHEDULE_TIME_WEEK),
        args=[bot],
        id="send_timetable",
        replace_existing=True,
        timezone="Asia/Novosibirsk"
    )
    logging.info("Еженедельный планировщик настроен")
    scheduler.start()

#EVERY DAY USER
async def send_user_everyday_to_group(bot: Bot):
    try:
        if GROUP_CHAT_ID is None:
            logging.warning("id чата не установлен")
            return
        user_today_message = get_today_assignment()
        await bot.send_message(chat_id=GROUP_CHAT_ID, text=user_today_message)
        logging.info("Ежедневное сообщение отправлено в чат")
    except Exception as e:
        logging.error(f"Ошибка при отправлке ежедневного сообщения {e}")

def setup_everyday_scheduler(bot: Bot):
    if not SCHEDULE_TIME_EVERY_DAY or len(SCHEDULE_TIME_EVERY_DAY.split())!=5:
        logging.error("SCHEDULE_TIME_EVERY_DAY имеет неверный формат")
        return
    scheduler.add_job(
        send_user_everyday_to_group,
        trigger=CronTrigger.from_crontab(SCHEDULE_TIME_EVERY_DAY),
        args=[bot],
        id="send_user_timetable",
        replace_existing=True,
        timezone="Asia/Novosibirsk"
    )
    logging.info("Ежедневный планировщик настроен")

    
