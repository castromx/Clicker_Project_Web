from celery import Celery

from database import database, crud, schemas
from database.database import DATABASE_URL, engine, Session
DATABASE_URL = DATABASE_URL
engine = engine
SessionLocal = Session

celery = Celery('tasks', broker='redis://localhost:6379')

@celery.task
def add_point_task(user_id: int, count: int):
    db = SessionLocal()
    score = crud.add_point(db, count, user_id)
    db.close()
    return score

@celery.task
def add_charge_count(db: Session, user_id: int, user.boosts.point):
    bosts = crud.get_user_boosts(db, user_id)
    bosts.charge_count += user.boosts.point
    db.commit()
    return bosts.charge_count
