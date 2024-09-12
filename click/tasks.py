from celery import Celery
from sqlalchemy.ext.asyncio import async_session
from database import crud


celery = Celery('tasks', broker='redis://localhost:6379')


@celery.task
async def add_charge_count(user_id: int):
    async with async_session() as session:
        async with session.begin():
            boosts = await crud.get_user_boosts(session, user_id)
            boosts.charge_count += 1
            await session.commit()
        return boosts.charge_count
