from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram import Bot
from schedule_service import generate_timetable_message, get_today_assignment
from config import GROUP_CHAT_ID, SCHEDULE_TIME_WEEK, SCHEDULE_TIME_EVERY_DAY
import logging
from storage import load_last_id_message_everyday, save_last_id_message_everyday

scheduler = AsyncIOScheduler(timezone = "Asia/Novosibirsk")

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

    trigger_time = CronTrigger.from_crontab(SCHEDULE_TIME_WEEK, timezone = "Asia/Novosibirsk")

    scheduler.add_job(
        send_timetable_to_group,
        trigger=trigger_time,
        args=[bot],
        id="send_timetable",
        replace_existing=True,
        misfire_grace_time = 3600
    )
    logging.info("Еженедельный планировщик настроен")

#EVERY DAY USER
async def send_user_everyday_to_group(bot: Bot):
    try:
        if GROUP_CHAT_ID is None:
            logging.warning("id чата не установлен")
            return
        
        last_id = load_last_id_message_everyday()
        if last_id:
            try:
                await bot.delete_message(chat_id=GROUP_CHAT_ID, message_id=last_id)
                logging.info("Вчерашнее напоминание удалено")
            except Exception as e:
                logging.warning(f"Не удалось удалить вчерашнее напоминание : {e}")




        user_today_message = get_today_assignment()
        msg = await bot.send_message(chat_id=GROUP_CHAT_ID, text=user_today_message)

        save_last_id_message_everyday(msg.message_id)

        logging.info("Ежедневное сообщение отправлено в чат")
    except Exception as e:
        logging.error(f"Ошибка при отправлке ежедневного сообщения {e}")

def setup_everyday_scheduler(bot: Bot):
    if not SCHEDULE_TIME_EVERY_DAY or len(SCHEDULE_TIME_EVERY_DAY.split())!=5:
        logging.error("SCHEDULE_TIME_EVERY_DAY имеет неверный формат")
        return

    trigger_time = CronTrigger.from_crontab(SCHEDULE_TIME_EVERY_DAY, timezone = "Asia/Novosibirsk")

    scheduler.add_job(
        send_user_everyday_to_group,
        trigger=trigger_time,
        args=[bot],
        id="send_user_timetable",
        replace_existing=True,
        misfire_grace_time = 3600
    )
    logging.info("Ежедневный планировщик настроен")

    
