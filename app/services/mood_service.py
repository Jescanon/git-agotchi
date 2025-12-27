from sqlalchemy import update

from app.models.user import Agotchi as AgotchiModel

from app.core.database import async_session

async def inf_about_mood(user_agatochi: AgotchiModel):
    async with async_session() as session:
        if 25 < user_agatochi.hp <= 75:
            mood = "Angry"
        elif user_agatochi.hp > 75:
            mood = "Happy"
        else:
            mood = "Dead"

        await session.execute(
            update(AgotchiModel)
            .where(AgotchiModel.user_id == user_agatochi.user_id)
            .values(mood=mood)
        )
        await session.commit()
        return mood
