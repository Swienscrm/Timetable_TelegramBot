import random
from config import USERS
import json
from pathlib import Path
from datetime import datetime


MAX_DAYS_PER_USER = 2
DAYS = ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"]

SCHEDULE_FILE = Path("schedule.json")

def generate_timetable() -> dict[str, str]:
    user_timetable = []
    user_days_count = {user: 0 for user in USERS}

    while len(user_timetable)<len(DAYS):
        random_user = random.choice(USERS)
        if user_days_count[random_user] < MAX_DAYS_PER_USER:
            user_timetable.append(random_user)
            user_days_count[random_user]+=1

    return {day: user for day, user in zip(DAYS, user_timetable)}

def save_schedule(schedule: dict[str,str]) -> None:
    SCHEDULE_FILE.write_text(
        json.dumps(schedule, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

def format_schedule_message(schedule: dict[str,str]):
    lines = ["РАСПИСАНИЕ ВЫБРОСА МУСОРА", ""]
    for day in DAYS:
        lines.append(f"{day} : {schedule[day]}")
    lines.append("")
    lines.append("Вы можете генерировать новое расписание командой /timetable")
    return "\n".join(lines)

def generate_timetable_message() -> str:
    schedule = generate_timetable()
    save_schedule(schedule)
    return format_schedule_message(schedule)

def load_schedule() -> dict[str, str] | None:
    if not SCHEDULE_FILE.exists():
        return None
    
    data = json.loads(SCHEDULE_FILE.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return None

    schedule: dict[str, str] = {}
    for k, v in data.items():
        if isinstance(k,str) and isinstance(v,str):
            schedule[k] = v
    return schedule

def get_today_assignment() -> str:
    schedule = load_schedule()
    if schedule is None:
        return "Расписание еще не сгенерировано"

    today_weekday = datetime.now().weekday()
    today_day_name = DAYS[today_weekday]

    user = schedule.get(today_day_name)
    if not user:
        return "Дежурный не найден сгенерируйте новое расписание"

    return f"НАПОМИНАНИЕ\n\nСегодня мусор выкидывает: {user}"

