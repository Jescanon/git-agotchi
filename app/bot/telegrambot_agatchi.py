from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select, update

from aiogram.fsm.context import FSMContext

from app.core.database import async_session

from app.models.user import User as UserModel, Agotchi as AgotchiModel

from app.api.routes import get_inf
from .telegram_utils import NameStates

from app.services.validate_time import get_time

user_router = Router()

@user_router.message(F.data == "create_agatochi")
async def create_agatochi(message: Message, state: FSMContext, callback: CallbackQuery):

    await state.set_state(NameStates.waiting_for_agatchi_name)

    await callback.message.answer("Введите имя вашему git-agatchi в следующем сообщении")

    await callback.answer("Начало изменения аккаунта GitHub...")

    async with async_session() as session:
        agatochi = AgotchiModel(user_id=message.from_user.id, )

    pass

@user_router.message(NameStates.waiting_for_agatchi_name, F.text)
async def agatochi_handler(message: Message, state: FSMContext):
    pass