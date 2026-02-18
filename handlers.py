from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from schedule_service import generate_timetable_message, get_today_assignment


router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Чтобы сгенерировать расписание используйте команду /timetable\n Чтобы узнать кто выносит мусор сегодня используйте команду /today")

@router.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer("Команды:\n/timetable — новое расписание")

@router.message(Command("timetable"))
async def timetable_cmd(message: Message):
    await message.answer(generate_timetable_message())

@router.message(Command("today"))
async def today_cmd(message: Message):
    await message.answer(get_today_assignment())