from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select, update

from aiogram.fsm.context import FSMContext

from app.core.database import async_session

from app.models.user import User as UserModel, Agotchi as AgotchiModel

from app.api.routes import get_inf
from .telegram_utils import NameStates, agatochi

from app.services.validate_time import get_time

user_router = Router()

@user_router.callback_query(F.data == "create_agatochi")
async def create_agatochi(callback: CallbackQuery, state: FSMContext):
    async with async_session() as session:
        info = await session.scalars(select(AgotchiModel).where(AgotchiModel.user_id == callback.from_user.id))
        res = info.first()
        if not res:
            new_agatochi = AgotchiModel(user_id=callback.from_user.id)

            session.add(new_agatochi)
            await session.commit()

    await state.set_state(NameStates.waiting_for_agatchi_name)

    await callback.message.answer("Введите имя вашему git-agatchi в следующем сообщении")

    await callback.answer()



@user_router.message(NameStates.waiting_for_agatchi_name, F.text)
async def agatochi_add_name(message: Message, state: FSMContext):
    user_id = message.from_user.id
    name = message.text.strip()

    if name.startswith('/'):
        return await message.answer("Пожалуйста, введите никнейм, а не команду.")

    async with async_session() as session:
        await session.execute(update(AgotchiModel).where(AgotchiModel.user_id == user_id).values(name=name))
        await session.commit()

    await state.clear()
    await message.answer(f"Задано имя для вашего питомца: {name}")

    return await show_photo(message)


@user_router.callback_query(F.data == "update_name")
async def update_agatochi_name(callback: CallbackQuery, state: FSMContext):
    await state.set_state(NameStates.waiting_for_agatchi_name)
    await callback.message.answer("Введите новое имя для вашего git‑agatchi:",)
    await callback.answer()

@user_router.message(Command("show_agatochi"))
async def show_photo(message: Message):
    async with async_session() as session:
        inf = await session.scalars(select(AgotchiModel).where(AgotchiModel.user_id == message.from_user.id))
        res = inf.first()

    text = f"{res.name}: Приветствую Вас, хозяин, о чем хотим пообщаться?"

    try:
        photo = res.photo
    except AttributeError:
        photo = "https://avatars.mds.yandex.net/i?id=af11ac927c419348eaea9c43b9d24955_l-4457245-images-thumbs&n=13"

    return await message.answer_photo(photo=photo,
        caption=text,
        reply_markup=agatochi(),
        parse_mode="Markdown"
    )