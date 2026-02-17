import random
from config import USERS
MAX_DAYS_PER_USER = 2
DAYS = ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"]

def generate_timetable_message() -> str:
    user_timetable = []
    user_days_count = {user: 0 for user in USERS}

    while len(user_timetable)<len(DAYS):
        random_user = random.choice(USERS)
        if user_days_count[random_user]<MAX_DAYS_PER_USER:
            user_timetable.append(random_user)
            user_days_count[random_user]+=1

    message = "РАСПИСАНИЕ ВЫБРОСА МУСОРА\n\n"

    for i in range(len(DAYS)):
        message += f"{DAYS[i]} : {user_timetable[i]}\n"
        
    message += "\nВы можете генерировать новое расписание командой /timetable"
    return message


