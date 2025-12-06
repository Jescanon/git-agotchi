from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup

def get_start_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Начать регистрацию", callback_data="start_registration")
    return builder.as_markup()

def dashboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Обновить", callback_data="profile_refresh")
    builder.button(text="Изменить GitHub", callback_data="start_registration")
    builder.button(text="Удалить аккаунт", callback_data="profile_delete")

    builder.adjust(2, 1)

    return builder.as_markup()

class RegistrationStates(StatesGroup):
    waiting_for_github_name = State()