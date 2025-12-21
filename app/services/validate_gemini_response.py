from app.services.gemini_service import analyze_code
from app.api.github_api import get_request
from aiogram.types import CallbackQuery

async def get_info_from_gemini(name, callback: CallbackQuery):
    await callback.message.answer(f"Идет анализ, чтобы покритиковать Вас 🤢")

    info_from_github = await get_request(name=name)

    if not info_from_github:
        return f"Ошибочка вышла, ну бывает"

    info_from_gemini = await analyze_code(info_from_github)

    comments = info_from_gemini.get("comments") or []

    await callback.message.answer(f"{info_from_gemini.get('summary')}")

    text = "\n".join(comments) if comments else "Недочётов не найдено 😎"

    await callback.message.answer(
        f"Какие ГРЕХИ 🤔:\n{text}"
    )
    return info_from_gemini
