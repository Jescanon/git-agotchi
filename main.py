import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import asyncio
from aiogram import Bot, Dispatcher
from app.config import get_settings

from app.api.github_api import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello"}


bot = Bot(token=get_settings().token)
dp = Dispatcher()


async def main():
    print("Бот запускается")
    from app.bot.telegrambot_user import user_router
    from app.bot.telegrambot_agatchi import user_router as agatochi_router
    dp.include_router(user_router)
    dp.include_router(agatochi_router)

    try:
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        print(f"Ошибка {e}")
    finally:
        await bot.session.close()

app.include_router(router)

if __name__ == "__main__":
    asyncio.run(main())
