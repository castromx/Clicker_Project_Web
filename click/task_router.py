from fastapi import APIRouter, BackgroundTasks
from tasks import add_point_task, add_charge_count
router = APIRouter()

@router.post('/add_celery_point/{user_id}')
async def add_point_endpoint(user_id: int, count: int):
    add_point_task.delay(user_id, count)
    return {"message": "Add point tadsk has been added to the queue."}

@router.post('/add_celery_charge/{user_id}')
async def add_charge_count(user_id: int, count: int):
    add_charge_count.delay(user_id, count)
    return {"message": "Add point tadsk has been added to the queue."}
