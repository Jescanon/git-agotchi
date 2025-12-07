from datetime import datetime

async def get_time():
    time = datetime.now().hour
    if time < 12:
        return f"Доброе утро"
    elif time < 19:
        return "Доброго вечера"
    return "Доброй ночи"