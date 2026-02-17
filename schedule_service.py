import random


def generate_timetable_message() -> str:
    USERS = ["Женя","Никита","Матвей","Коля"]
    DAYS = ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"]
    user_timetable = []
    count_zheka=count_nikita=count_matvey=count_kolya=0
    while len(user_timetable)<7:
        random_user = random.choice(USERS)
        if random_user == "Женя" and count_zheka<2:
            user_timetable.append(random_user)
            count_zheka+=1
        elif random_user == "Никита" and count_nikita<2:
            user_timetable.append(random_user)        
            count_nikita+=1
        elif random_user == "Матвей" and count_matvey<2:
            user_timetable.append(random_user)        
            count_matvey+=1
        elif random_user == "Коля" and count_kolya<2:
            user_timetable.append(random_user)
            count_kolya+=1
    message = "РАСПИСАНИЕ ВЫБРОСА МУСОРА\n\n"
    for i in range(len(DAYS)):
        message += f"{DAYS[i]} : {user_timetable[i]}\n"
    message += "\nВы можете генерировать новое расписание командой /timetable"
    return message


