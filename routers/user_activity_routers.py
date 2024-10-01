from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from database import schemas, crud
from database.database import get_async_session


router = APIRouter()


@router.post("/div_point")
async def div_user_point(user_id: int, price: int, db: AsyncSession = Depends(get_async_session)):
    point = await crud.get_user_scores(db, user_id)
    point = point.score
    if point > price:
        await crud.div_points(db, user_id, price)
        return {"status": "success"}
    raise HTTPException(status_code=422, detail="Not enough points")


@router.post("/buy_fill_char_count")
async def buy_fill_char(user_id: int, db: AsyncSession = Depends(get_async_session)):
    point = await crud.get_user_scores(db, user_id)
    point = point.score
    price = point * 10
    if point > price:
        await crud.div_points(db, user_id, price)
        return await crud.buy_fill_char(db, user_id)
    raise HTTPException(status_code=422, detail="Not enough points")


@router.post("/buy_charge_count")
async def buy_charge(user_id: int, db: AsyncSession = Depends(get_async_session)):
    point = await crud.get_user_scores(db, user_id)
    point = point.score
    price = point * 10
    if point > price:
        await crud.div_points(db, user_id, price)
        return await crud.buy_charge_count(db, user_id)
    raise HTTPException(status_code=422, detail="Not enough points")


@router.post("/buy_mine_coint")
async def buy_mine(user_id: int, db: AsyncSession = Depends(get_async_session)):
    point = await crud.get_user_scores(db, user_id)
    point = point.score
    price = point * 10
    if point > price:
        await crud.div_points(db, user_id, price)
        return await crud.buy_mine_coint(db, user_id)
    raise HTTPException(status_code=422, detail="Not enough points")


@router.get("/get_user_achivments", response_model=schemas.Achivments)
async def get_user_achivments(user_id: int, db: AsyncSession = Depends(get_async_session)):
    return await crud.get_user_achivments(db, user_id)


@router.post("/fill_charge_count")
async def fill_charge(user_id: int, point: int, db: AsyncSession = Depends(get_async_session)):
    boosts = await crud.get_user_boosts(db, user_id)
    charge_lvl = boosts.charge_count
    charge = await crud.get_user_charge(db, user_id)
    max_charge = charge_lvl * 5000
    if charge < max_charge:
        await crud.add_charge_point(db, user_id, point)
    return {"fill": "full"}



@router.post("/start-game/{user_id}")
async def start_fill_charge(user_id: int, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_async_session)):
    background_tasks.add_task(crud.refilling_charge, db, user_id)
    return {"message": "Charge filled successfully"}