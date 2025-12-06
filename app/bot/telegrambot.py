from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select, update

from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, InputMediaPhoto

from app.core.database import async_session

from app.models.user import User as UserModel

from app.api.routes import get_inf
from .telegram_utils import get_start_keyboard, RegistrationStates, dashboard


user_router = Router()


@user_router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "Добро пожаловать! Чтобы зарегистрироваться и привязать ваш аккаунт GitHub, нажмите кнопку ниже:",
        reply_markup=get_start_keyboard()
    )

@user_router.callback_query(F.data == "start_registration")
async def help_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id

    async with async_session() as session:
        result = await session.scalars(select(UserModel).where(UserModel.telegram_id == user_id))
        user = result.first()

        if not user:
            user = UserModel(telegram_id=user_id)
            session.add(user)
            await session.commit()

    await state.set_state(RegistrationStates.waiting_for_github_name)

    await callback.message.edit_text(
        "Введите свой никнейм на GitHub в следующем сообщении."
    )


@user_router.message(RegistrationStates.waiting_for_github_name, F.text)
async def process_github_name_input(message: Message, state: FSMContext):
    user_id = message.from_user.id
    github_name_input = message.text.strip()

    if github_name_input.startswith('/'):
        return await message.answer("Пожалуйста, введите никнейм, а не команду.")

    info_github = await get_inf(github_name_input)

    if not info_github:
        return await message.answer(
            f"Пользователь GitHub с никнеймом {github_name_input} не найден. Попробуйте ввести никнейм еще раз."
        )


    async with async_session() as session:
        await session.execute(update(UserModel).
                              where(UserModel.telegram_id == user_id).
                              values(github_name=info_github))
        await session.commit()

    await state.clear()

    return await message.answer(
        f"Поздравляем! Вы успешно зарегистрировали свой никнейм {info_github}."
    )


@user_router.message(Command("show_dashboard"))
async def send_dashboard(message: Message):
    caption_text = (
        f"🤖 **ВАШ ГИТ-ТАМАГОЧИ**\n"
        f"Статистика: 12 коммитов за неделю.\n"
    )

    await message.answer_photo(
        photo="https://otvet.mail.ru/mm-proxy/mail/burgomistr1970/_cover/i-415.jpg",
        caption=caption_text,
        reply_markup=dashboard(),
        parse_mode="Markdown"
    )
