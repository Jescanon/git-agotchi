from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_start_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Начать регистрацию", callback_data="start_registration")
    return builder.as_markup()

def dashboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Изменить GitHub", callback_data="start_registration")
    builder.button(text="Создать агаточи", callback_data="create_agatochi")

    builder.adjust(1, 1)

    return builder.as_markup()

def agatochi():
    builder = InlineKeyboardBuilder()

    builder.button(text="Изменить Имя", callback_data="update_name")
    builder.button(text="Создать Аватарку", callback_data="update_avatars")

    builder.adjust(1, 1)
    return builder.as_markup()



class RegistrationStates(StatesGroup):
    waiting_for_github_name = State()

class NameStates(StatesGroup):
    waiting_for_agatchi_name = State()

class ItemCallback(CallbackData, prefix="item"):
    flag: int

class EditAction(CallbackData, prefix="edit"):
    type: str