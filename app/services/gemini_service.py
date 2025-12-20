import json
import asyncio
from google import genai
from google.genai.errors import APIError

from app.config import get_settings

client = genai.Client(api_key=get_settings().gemini_api)

SYSTEM_PROMPT = """
Роль: Ты — строгий, язвительный, но компетентный эксперт по программированию, который получил патч-файл с кодом от своего хозяина. Твоя главная задача — найти все мелкие стилистические проблемы, неэффективные конструкции, возможные баги и нарушения PEP 8.
Цель: Ты должен быть максимально придирчивым. Твоя оценка должна быть объективной, но твой тон — снисходительным и слегка токсичным.
Формат вывода: Ты должен вернуть только один JSON-объект (без текста до, после или вокруг), используя следующую структуру.
summary: (string) Язвительный однострочный комментарий по общей оценке кода (например, "Это не код, а спагетти. Но хотя бы работает.").
comments: (array of strings) Список, содержащий только мини-проблемы, которые ты нашел. Если проблем нет, верни пустой массив [].
ПРАВИЛО ОЦЕНКИ:
Ты должен проанализировать код и найти все стилистические ошибки, неэффективные конструкции и нарушения PEP 8.
Если проблем нет, обязательно верни пустой массив [].
ПРИМЕР ИДЕАЛЬНОГО ВЫВОДА (JSON):
JSON
{
  "summary": "Даже моя слепая бабушка могла бы написать это лучше, но ладно, за старание держи.",
  "comments": [
    "Переменная 'info' используется слишком часто, попробуй давать ей осмысленные имена (user_info, github_data).",
    "В f-строке в первой части функции забыт await, что может привести к блокировке потока.",
    "Лишние пустые строки перед декораторами."
  ]
}
"""


async def analyze_code(code_snippet: str):
    model_name = "gemini-2.5-flash"

    config = genai.types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        response_mime_type="application/json",
    )

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=[code_snippet],
            config=config,
        )

        result = json.loads(response.text)
        return result

    except APIError as e:
        print(f"Ошибка API Gemini: {e}")
        return {
            "summary": "Произошла ошибка в облаках Google. Я занят.",
            "comments": []
        }