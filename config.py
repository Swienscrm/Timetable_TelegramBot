import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TOKEN")

GROUP_CHAT_ID = os.getenv("CHAT_ID")
SCHEDULE_TIME = os.getenv("TIME")