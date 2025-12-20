from app.services.gemini_service import analyze_code
from app.api.github_api import get_request


async def get_info_from_gemini(name):
    info_from_github = await get_request(name=name)

    if not info_from_github:
        return f"Ошибочка вышла, ну бывает"

    info_from_gemini = await analyze_code(info_from_github)

    return info_from_gemini
