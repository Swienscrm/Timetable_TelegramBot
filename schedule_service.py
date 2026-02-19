import random
from config import USERS
import json
from pathlib import Path
from datetime import datetime
from storage import load_excluded


DAYS = ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"]

SCHEDULE_FILE = Path("schedule.json")



def get_active_user() -> list[str]:
    excluded = load_excluded()
    return [u for u in USERS if u not in excluded]

def calc_max_day_per_user(days_count: int, user_count: int) -> int:
    if user_count == 0:
        return 0
    return (days_count + user_count-1) // user_count

def generate_timetable(active_users: list[str] | None = None) -> dict[str, str]:
    if active_users is None:
        active_users = get_active_user()
    if not active_users:
        raise RuntimeError("Нет активных пользователей для генерации расписания")

    MAX_DAYS_PER_USER = calc_max_day_per_user(len(DAYS), len(active_users))
    user_timetable: list[str] = []
    user_days_count = {u: 0 for u in active_users}

    max_attempts = 10_000
    attempts = 0

    while len(user_timetable)<len(DAYS):
        attempts += 1
        if attempts > max_attempts:
            raise RuntimeError("Не удалость составить расписание, слишком много попыток")
        u = random.choice(active_users)
        if user_days_count[u] < MAX_DAYS_PER_USER:
            user_timetable.append(u)
            user_days_count[u]+=1

    return {day: u for day, u in zip(DAYS, user_timetable)}

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

