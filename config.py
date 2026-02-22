import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TOKEN")
if not BOT_TOKEN:
    raise ValueError("Токен не найден")

GROUP_CHAT_ID = int(os.getenv("CHAT_ID"))


SCHEDULE_TIME_WEEK = os.getenv("TIME_WEEK", "0 12 * * mon")
SCHEDULE_TIME_EVERY_DAY = os.getenv("TIME_EVERY_DAY", "0 22 * * *")

raw_users = os.getenv("FRIENDS", "Женя,Никита,Матвей,Коля")
USERS = [name.strip() for name in raw_users.split(",") if name.strip()]