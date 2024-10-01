import asyncio

from sqlalchemy.orm import joinedload, selectinload
from datetime import datetime
from . import schemas, models
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user(db: AsyncSession, user: schemas.UserAccount):
    time_now = datetime.utcnow()
    user_data = user.dict(exclude={"register_at", "last_login_at", "scores", "charges"})
    db_user = models.User(**user_data, register_at=time_now, last_login_at=time_now)
    db.add(db_user)
    try:
        await db.commit()
    except Exception as e:
        print('User Already Exists')
    else:
        await db.refresh(db_user)
        return db_user


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    return result.scalars().first()


async def get_user_tg_id_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    return result.scalars().first().tg_id


async def get_all_users(db: AsyncSession):
    result = await db.execute(select(models.User))
    return result.scalars().all()


async def create_user_score(db: AsyncSession, user_id: int):
    user = await get_user(db, user_id)
    if user is None:
        return None
    scores = models.UserScore(user_id=user.id, score=0)
    db.add(scores)
    await db.commit()
    await db.refresh(scores)
    return scores


async def get_user_scores(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.UserScore).filter(models.UserScore.user_id == user_id))
    return result.scalars().first()


async def add_point(db: AsyncSession, count: int, user_id: int):
    score_user = await get_user_scores(db, user_id)
    if score_user is None:
        return None
    score_user.score += count
    db.add(score_user)
    await db.commit()
    await db.refresh(score_user)
    return score_user


async def create_user_boost(db: AsyncSession, user_id: int):
    user = await get_user(db, user_id)
    if user is None:
        return None
    boosts = models.Boosts(user_id=user.id, fill_char_count=1, charge_count=1, mine_coint=1)
    db.add(boosts)
    await db.commit()
    await db.refresh(boosts)
    return boosts


async def get_user_boosts(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.Boosts).filter(models.Boosts.user_id == user_id))
    return result.scalars().first()


async def dev_charge(db: AsyncSession, user_id: int):
    boosts = await get_user_boosts(db, user_id)
    if boosts is None:
        return None
    count_miner = boosts.mine_coint
    boosts.charge_count -= count_miner
    await db.commit()
    return boosts.charge_count


async def create_image(db: AsyncSession, image_data: bytes):
    db_image = models.Image(data=image_data)
    db.add(db_image)
    await db.commit()
    await db.refresh(db_image)
    return db_image


async def create_clan(db: AsyncSession, clan: schemas.ClanCreate):
    db_clan = models.Clan(**clan.dict())
    db.add(db_clan)
    await db.commit()
    await db.refresh(db_clan)
    if clan.img_id:
        stmt = select(models.Image).filter(models.Image.id == clan.img_id)
        result = await db.execute(stmt)
        db_image = result.scalars().first()
        if db_image:
            db_clan.image = db_image
            await db.commit()
            await db.refresh(db_clan)
    return db_clan


async def get_clan(db: AsyncSession, clan_id: int):
    result = await db.execute(select(models.Clan).filter(models.Clan.id == clan_id))
    return result.scalars().first()


async def create_clan_score(db: AsyncSession, clan_id: int):
    clan = await get_clan(db, clan_id)
    if clan is None:
        return None
    scores = models.ClanScore(clan_id=clan.id, score=0)
    db.add(scores)
    await db.commit()
    await db.refresh(scores)
    return scores


async def get_clan_scores(db: AsyncSession, clan_id: int):
    result = await db.execute(select(models.ClanScore).filter(models.ClanScore.clan_id == clan_id))
    return result.scalars().first()


async def add_clan_point(db: AsyncSession, clan_id: int):
    score_clan = await get_clan_scores(db, clan_id)
    if score_clan is None:
        return None
    score_clan.score += 1
    db.add(score_clan)
    await db.commit()
    await db.refresh(score_clan)
    return score_clan


async def enter_in_clan(db: AsyncSession, clan_id: int, user_id: int):
    db_clan_enter = models.UsersClan(user_id=user_id, clan_id=clan_id)
    db.add(db_clan_enter)
    await db.commit()
    await db.refresh(db_clan_enter)
    return db_clan_enter


async def get_clans_for_user(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(models.Clan)
        .join(models.UsersClan)
        .filter(models.UsersClan.user_id == user_id)
        .options(selectinload(models.Clan.count_score))
    )

    return result.scalars().first()


async def leave_from_clan(db: AsyncSession, user_id: int):
    user_clan_record = await db.execute(select(models.UsersClan).filter(models.UsersClan.user_id == user_id))
    user_clan_record = user_clan_record.scalars().first()
    if user_clan_record:
        await db.delete(user_clan_record)
        await db.commit()
        return {"msg": "The user has left the clan"}
    else:
        return None


async def get_clans(db: AsyncSession):
    result = await db.execute(select(models.Clan).join(models.UsersClan).options(joinedload(models.Clan.count_score)))
    return result.scalars().all()


async def get_image(db: AsyncSession, image_id: int):
    result = await db.execute(select(models.Image).filter(models.Image.id == image_id))
    return result.scalars().first()


async def get_clan_members(db: AsyncSession, clan_id: int):
    result = await db.execute(select(models.User)
                              .join(models.UsersClan)
                              .filter(models.UsersClan.clan_id == clan_id)
                              .options(joinedload(models.User.scores)))
    return result.scalars().all()


async def get_leader_users(db: AsyncSession):
    result = await db.execute(select(models.User)
                              .join(models.UserScore, models.User.id == models.UserScore.user_id)
                              .order_by(models.UserScore.score.desc())
                              .options(joinedload(models.User.scores)))
    return result.scalars().all()


async def get_leader_clans(db: AsyncSession):
    result = await db.execute(select(models.Clan)
                              .join(models.ClanScore, models.Clan.id == models.ClanScore.clan_id)
                              .order_by(models.ClanScore.score.desc())
                              .options(joinedload(models.Clan.count_score)))
    return result.scalars().all()


async def div_points(db: AsyncSession, user_id: int, price: int):
    points = await get_user_scores(db, user_id)
    if points is None:
        return None
    points.score -= price
    await db.commit()
    return points.score


async def buy_fill_char(db: AsyncSession, user_id: int):
    bosts = await get_user_boosts(db, user_id)
    if bosts is None:
        return None
    if bosts.fill_char_count < 3:
        bosts.fill_char_count += 1
        await db.commit()
        return bosts.fill_char_count
    return bosts.fill_char_count


async def buy_charge_count(db: AsyncSession, user_id: int):
    bosts = await get_user_boosts(db, user_id)
    if bosts is None:
        return None
    if bosts.charge_count < 3:
        bosts.charge_count += 1
        await db.commit()
        return bosts.charge_count
    return bosts.charge_count


async def buy_mine_coint(db: AsyncSession, user_id: int):
    bosts = await get_user_boosts(db, user_id)
    if bosts is None:
        return None
    if bosts.mine_coint < 3:
        bosts.mine_coint += 1
        await db.commit()
        return bosts.mine_coint
    return bosts.mine_coint


async def create_user_achivments(db: AsyncSession, user_id: int):
    user = await get_user(db, user_id)
    if user is None:
        return None
    achivments = models.UserAchivments(user_id=user.id, up_50k=False, up_100k=False, up_500k=False, up_1million=False)
    db.add(achivments)
    await db.commit()
    await db.refresh(achivments)
    return achivments


async def get_user_achivments(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.UserAchivments).filter(models.UserAchivments.user_id == user_id))
    return result.scalars().first()


async def create_user_charge(db: AsyncSession, user_id: int):
    user = await get_user(db, user_id)
    if user is None:
        return None
    charge = models.UserCharges(user_id=user.id, charge=5000)
    db.add(charge)
    await db.commit()
    await db.refresh(charge)
    return charge


async def get_user_charge(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.UserCharges).filter(models.UserCharges.user_id == user_id))
    return result.scalars().first()


async def add_charge_point(db: AsyncSession, user_id: int, points: int):
    charge = await get_user_charge(db, user_id)
    if charge is None:
        return None
    charge.charge += points
    db.add(charge)
    await db.commit()
    await db.refresh(charge)
    return charge.charge


async def div_charge_point(db: AsyncSession, user_id: int, points: int):
    charge = await get_user_charge(db, user_id)
    if charge is None:
        return None
    charge.charge -= points
    db.add(charge)
    await db.commit()
    await db.refresh(charge)
    return charge.charge



async def refilling_charge(db: AsyncSession, user_id: int):
    while True:
        charge = await get_user_charge(db, user_id)
        if charge is not None and charge.charge < 5000:
            charge.charge += 1
            db.add(charge)
            await db.commit()
            await db.refresh(charge)
        await asyncio.sleep(1)
