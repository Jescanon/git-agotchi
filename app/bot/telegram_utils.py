from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup

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

class RegistrationStates(StatesGroup):
    waiting_for_github_name = State()

class NameStates(StatesGroup):
    waiting_for_agatchi_name = State()