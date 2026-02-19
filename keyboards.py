from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import USERS
from storage import load_excluded

def friends_toggle_keyboard():
    excluded = load_excluded()
    kb = InlineKeyboardBuilder()

    for user in USERS:
        enable = user not in excluded
        label = f"{'✅' if enable else '❌'} {user}"
        kb.button(text = label, callback_data = f"toggle_friends:{user}")

    kb.adjust(2)
    return kb.as_markup()