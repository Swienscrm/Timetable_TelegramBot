from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import CommandStart, Command
from config import USERS
from schedule_service import generate_timetable_message, get_today_assignment
from storage import toggle_user_excluded, load_excluded
from keyboards import friends_toggle_keyboard
import logging


router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Чтобы сгенерировать расписание используйте команду /timetable\n Чтобы узнать кто выносит мусор сегодня используйте команду /today\nЧтобы управлять людьми в генерации расписания /friends")

@router.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer("Команды:\n/timetable — новое расписание\n/friends - выключить или включить человека в расписание")

@router.message(Command("timetable"))
async def timetable_cmd(message: Message):
    await message.answer(generate_timetable_message())

@router.message(Command("today"))
async def today_cmd(message: Message):
    await message.answer(get_today_assignment())

@router.message(Command("friends"))
async def friends_cmd(message: Message):
    await message.answer("Включи или выключи друзей из расписания", reply_markup=friends_toggle_keyboard())

@router.message(Command("id"))
async def chat_id_cmd(message: Message):
    logging.info(f"Chat ID: {message.chat.id}")

@router.callback_query(lambda c: c.data and c.data.startswith("toggle_friends:"))
async def toogle_friend_cb(callback: CallbackQuery):
    user = callback.data.split(":",1)[1]
    toggle_user_excluded(user)

    excluded = load_excluded()
    active = [u for u in USERS if u not in excluded]

    await callback.message.edit_text(
        "Включи или выключи друзей из расписания:\n\n"
        f"Активные друзья: {', '.join(active) if active else 'никого'}",
        reply_markup=friends_toggle_keyboard()
    ) 
    await callback.answer()