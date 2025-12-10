import uvicorn
from fastapi import FastAPI

import asyncio
from aiogram import Bot, Dispatcher
from app.config import get_settings



app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


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

if __name__ == "__main__":
    asyncio.run(main())
