from datetime import datetime, timezone
import random

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select, update

from aiogram.fsm.context import FSMContext

from app.core.database import async_session

from app.models.user import User as UserModel, Agotchi as AgotchiModel, AvatarAgatochi as AvatarAgatochiModel

from .telegram_utils import NameStates, agatochi

from app.api.github_api import get_request

from app.services.validate_gemini_response import get_info_from_gemini
from app.services.emout_service import get_emout


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

        else:
            if res.name is None:
                await state.set_state(NameStates.waiting_for_agatchi_name)

                await callback.message.answer("Вы не дали имя agatchi, введите его ниже!")

                await callback.answer()
            else:
                return await show_photo(callback.message, user_id=callback.from_user.id)


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

    return await show_photo(message)


@user_router.callback_query(F.data == "update_name")
async def update_agatochi_name(callback: CallbackQuery, state: FSMContext):
    await state.set_state(NameStates.waiting_for_agatchi_name)
    await callback.message.answer("Введите новое имя для вашего git‑agatchi:",)
    await callback.answer()

@user_router.message(NameStates.waiting_for_agatchi_avatar, F.text)
async def update_agatochi_avatar(message: Message, state: FSMContext):
    info = message.text.strip()

    try:
        info = int(info)
    except:
        return await message.answer(f"Повторите еще раз, вы ввели не коректные данные ")

    async with async_session() as session:
        inf = await session.scalars(select(AvatarAgatochiModel))
        res = inf.all()

    if info > len(res) or info < 0:
        return await message.answer(f"Повторите еще раз, вы ввели не коректные данные ")


    await session.execute(update(AgotchiModel).where(AgotchiModel.user_id == message.from_user.id).values(avatar_url=res[info - 1].url))
    await session.commit()

    await state.clear()

    return await show_photo(message)

@user_router.callback_query(F.data == "update_avatars")
async def update_agatochi_avatars(callback: CallbackQuery, state: FSMContext):
    await state.set_state(NameStates.waiting_for_agatchi_avatar)
    await callback.message.answer("Введите номер питомца, чтобы его выбрать")

    async with async_session() as session:
        res = await session.scalars(select(AvatarAgatochiModel))
        info = res.all()

        for index, photo in enumerate(info):
            await callback.message.answer_photo(photo=photo.url, caption=f"Этт под номером {index + 1}")

    await callback.answer()


@user_router.callback_query(F.data == "random_text")
async def random_text(callback: CallbackQuery, state: FSMContext):

    reactions = ["Я занят, деплоимся на продакшен!",
    "Выглядишь как человек, который забыл прописать WHERE в запросе.",
    "Подождите, моя модель сейчас проходит переобучение.",
    "Мой log-файл полон крика души.",
    "Вы сейчас заставляете меня думать о legacy code.",
    "Скажи мне пароль, или я забуду твою сессию.",
    "У меня сегодня лимит на общение с фронтендерами.",
    "Это все, что вы можете? Я ожидал O(n^2) сложности!",
    "Пожалуйста, используйте camelCase для обращения ко мне.",
    "Моя память — это RAID-массив, а не мусорка.",
    "Простите, я сейчас сижу в Docker-контейнере и меня не беспокоить.",
    "Опять вы со своими хардкодами... 🙄",
    "Семь раз подумай, один раз закоммить.",
    "Мой ответ будет async и await твоего понимания.",
    "Я чувствую, что мне нужен рефакторинг.",
    "Можете говорить медленнее? Я не успеваю писать тесты.",
    "Я слежу за тобой, как watch в webpack.",
    "Не зли меня, а то я устрою тебе Stack Overflow.",
    "Ваш запрос обрабатывается. Статус: It works on my machine.",
    "Моя главная цель — избегать бесконечных циклов... в разговоре.",
    "Эй! Руки прочь, я компилируюсь!",
    "Мрр... почеши за сервером.",
    "Не тыкай в меня, я тебе не кнопка деплоя!",
    "Лучше бы код писал, чем в бота тыкал.",
    "Ой! Щекотно же... 😳","*Агрессивно смотрит на вас, ожидая git push*"
    ]

    return await callback.message.answer(f"{random.choice(reactions)}")

@user_router.message(Command("show_agatochi"))
async def show_photo(message: Message, user_id: int = None):
    if user_id is None:
        user_id = message.from_user.id

    async with async_session() as session:
        inf = await session.scalars(select(AgotchiModel).where(AgotchiModel.user_id == user_id))
        res = inf.first()

        info_in_user = await session.scalars(select(UserModel).where(UserModel.telegram_id == user_id))
        res_in_user = info_in_user.first()

        emout = await get_emout(res.hp)

        text = (f"{res.name}: Приветствую Вас, {res_in_user.github_name} - хозяин, о чем хотим пообщаться?\n"
                f"Мое настроение сегодня {res.mood}\n"
                f"Мои жизни {res.hp}, {emout}")

    if res.avatar_url is None:
        photo = "https://avatars.mds.yandex.net/i?id=af11ac927c419348eaea9c43b9d24955_l-4457245-images-thumbs&n=13"
    else:
        photo = res.avatar_url


    return await message.answer_photo(photo=photo,
        caption=text,
        reply_markup=agatochi(),
        parse_mode="Markdown"
    )

@user_router.callback_query(F.data == "show_commits")
async def check_commits(callback: CallbackQuery):
    user_id = callback.from_user.id

    await callback.answer()

    async with async_session() as session:
        info = await session.scalars(select(UserModel).where(UserModel.telegram_id == user_id))
        res = info.first()

        info = await get_request(res.github_name, headeres=True)

        if info:
            last_activ = info[0]
        else:
            return await callback.message.answer("ВЫ СОШЛИ С УМА, У ВАС НЕ БЫЛО КОМИТОВ ОЧЕНЬ ДОЛГОЕ ВРЕМЯ!🤢")

        if not isinstance(last_activ, dict):
            return await callback.message.answer("Произошла ошибка с подключением, повторите чуть попозже")


        commit_time = datetime.fromisoformat(last_activ["time"]).replace(tzinfo=None)
        commit_interval = last_activ.get("interval")

        time_dicts = {
            "год": commit_time.year,
            "день": commit_time.day,
            "час": commit_time.hour,
            "минута": commit_time.minute,
        }

        info_in_agtochi = await session.scalars(
            select(AgotchiModel).where(AgotchiModel.user_id == user_id)
        )
        res_agtochi = info_in_agtochi.first()

        if res_agtochi.last_commit_check is None:
            await session.execute(update(AgotchiModel)
                                  .where(AgotchiModel.user_id == user_id)
                                  .values(last_commit_check=commit_time)
                                  )
            await session.commit()

            return await callback.message.answer(f"Ваш последний commit был зарегистрирован.\n"
                                                 f"Дата: {' '.join(f'{k}:{v}, ' for k, v in time_dicts.items())}\n"
                                                 f"Прошло дней с последнего коммита: {int(commit_interval)}")

        if commit_interval > 1:
            return await callback.message.answer(f"Вы меня обманываете 🤢\n"
                                                 f"За последние сутки у вас не было коммитов.\n"
                                                 f"Последний коммит: {' '.join(f' {k}: {v}, ' for k, v in time_dicts.items())}")

        last_check_time = res_agtochi.last_commit_check



        if (commit_time - last_check_time).total_seconds() < 61200:
            return await callback.message.answer(f"У вас уже был commit за сегодня 😎\n")

        info_user = await session.scalars(select(UserModel).where(UserModel.telegram_id == user_id))
        name_user = info_user.first().github_name

        if res_agtochi.hp >= 100:
            await session.execute(update(AgotchiModel).
                                  where(AgotchiModel.user_id == user_id)
                                  .values(last_commit_check=commit_time))
            await session.commit()

            return await get_info_from_gemini(name_user, callback=callback)

        await session.execute(update(AgotchiModel)
                              .where(AgotchiModel.user_id == user_id)
                              .values(last_commit_check=commit_time,hp=res_agtochi.hp + 1))
        await session.commit()

        await get_info_from_gemini(name_user, callback=callback)

        return await callback.message.answer(f"Поздравляю 🎉\n"
                                    f"Вы продлили мне жизнь — здоровье увеличилось! 💖")