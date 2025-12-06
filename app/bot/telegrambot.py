from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from sqlalchemy import select, update

from app.core.database import async_session

from app.models.user import User as UserModel

from app.api.routes import get_inf



def register_handlers(dp):
    @dp.message(Command("start"))
    async def start_handler(message: Message):
        async with async_session() as session:
            inf = await session.scalars(select(UserModel).where(UserModel.telegram_id == message.from_user.id))
            if inf.first():
                return message.answer(f"Вы уже зарегистрированы.")

            user = UserModel(telegram_id=message.from_user.id)
            session.add(user)
            await session.commit()

        return await message.answer(f"Вы зарегистрировались в боте.")

    @dp.message(Command("register_name"))
    async def help_handler(message: Message, command: CommandObject):
        msg = command.args

        if msg is None:
            return await message.answer(f"Вы не указали никнейм, введите /register_name Имя")

        info_github = await get_inf(msg)
        if not info_github:
            return await message.answer(f"Такой пользователь GitHub не найден. Попробуйте еще раз.")

        async with async_session() as session:

            await session.scalars(update(UserModel).
                                        where(UserModel.telegram_id == message.from_user.id)
                                        .values(github_name=info_github))
            await session.commit()

        return await message.answer(f"Вы успешно зарагистрировали совой никнейм {info_github}")
