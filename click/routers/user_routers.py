from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from database import schemas, crud
from database.database import get_async_session
from database.models import User

router = APIRouter()


@router.post("/create_user", response_model=schemas.UserAccount)
async def create_user(user: schemas.UserAccount, db: AsyncSession = Depends(get_async_session)):
    db_user = await crud.create_user(db=db, user=user)
    if db_user:
        scores = await crud.create_user_score(db, db_user.id)
        await crud.create_user_boost(db, db_user.id)
        await crud.create_user_achivments(db, db_user.id)
        charges = await crud.create_user_charge(db, db_user.id)

        response_user = schemas.UserAccount(
            name=db_user.name,
            tg_id=db_user.tg_id,
            register_at=db_user.register_at,
            last_login_at=db_user.last_login_at,
            scores=scores,
            charges=charges
        )
        return response_user

    raise HTTPException(status_code=400, detail="User Already Exists")


@router.get("/get_user", response_model=schemas.UserAccount)
async def get_user(id_user: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(
        select(User).options(selectinload(User.scores), selectinload(User.charges)).filter_by(tg_id=id_user)
    )
    user = result.scalars().first()
    if user is None:
        return {"error": "User not found"}
    return user


@router.get("/get_all_users")
async def get_all_users(db: AsyncSession = Depends(get_async_session)):
    return await crud.get_all_users(db)


@router.get("/get_user_score")
async def get_user_score(user_id: int, db: AsyncSession = Depends(get_async_session)):
    return await crud.get_user_scores(db, user_id)


@router.post("/create_user_scores")
async def create_user_scores(user_id: int, db: AsyncSession = Depends(get_async_session)):
    return await crud.create_user_score(db, user_id)


@router.post("/add_user_scores")
async def add_user_scores(user_id: int, count: int, db: AsyncSession = Depends(get_async_session)):
    boosts = await crud.get_user_boosts(db, user_id)
    charge = boosts.charge_count * 600
    count = boosts.mine_coint * count
    if charge > 1:
        await crud.add_point(db, count, user_id)
        clan = await crud.get_clans_for_user(db, user_id)
        if clan:
            clan_id = clan.id
            await crud.add_clan_point(db, clan_id)
        await crud.div_charge_point(db, user_id, 1)
        charge_after = boosts.charge_count
        count_after = await crud.get_user_scores(db, user_id)
        return {"charge": charge_after, "count": count_after.score}
    raise HTTPException(status_code=422, detail="Energy charge too low")


@router.get("/get_user_boosts")
async def get_user_boosts(user_id: int, db: AsyncSession = Depends(get_async_session)):
    return await crud.get_user_boosts(db, user_id)


@router.get("/get_leaderboard_user")
async def get_leaderboard_user(db: AsyncSession = Depends(get_async_session)):
    return await crud.get_leader_users(db)


@router.get("/get_leaderboard_clan")
async def get_leaderboard_clan(db: AsyncSession = Depends(get_async_session)):
    return await crud.get_leader_clans(db)

