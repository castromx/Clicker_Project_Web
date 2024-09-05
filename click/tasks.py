from celery import Celery
from sqlalchemy.ext.asyncio import AsyncSession
from database import database, crud, schemas
from database.database import DATABASE_URL, get_async_session

celery = Celery('tasks', broker='redis://localhost:6379')

@celery.task
async def add_point_task(user_id: int, count: int):
    async with async_session() as session:  
        async with session.begin():
            score = await crud.add_point(session, count, user_id)
        return score

@celery.task
async def add_charge_count(user_id: int):
    async with async_session() as session:  
        async with session.begin():
            boosts = await crud.get_user_boosts(session, user_id)
            boosts.charge_count += 1
            await session.commit()  
        return boosts.charge_count
