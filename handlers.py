from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from schedule_service import generate_timetable_message

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Чтобы сгенерировать расписание используйте команду /timetable")

@router.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer("Команды:\n/timetable — новое расписание")

@router.message(Command("timetable"))
async def timetable_cmd(message: Message):
    await message.answer(generate_timetable_message())