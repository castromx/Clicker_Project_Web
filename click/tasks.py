from celery import Celery
from database import database, crud, schemas
from database.database import DATABASE_URL, engine, Session
DATABASE_URL = DATABASE_URL
engine = engine
SessionLocal = Session

celery = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task
def add_point_task(user_id: int, count: int):
    db = SessionLocal()
    score = crud.add_point(db, count, user_id)
    db.close()
    return score
