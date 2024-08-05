from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from . import schemas, models
from typing import List
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

# Функція для створення нового користувача
async def create_user(db: Session, user: schemas.UserAccount):
    time_now = datetime.utcnow()
    user_data = user.dict(exclude={"register_at", "last_login_at"})
    db_user = models.User(**user_data, register_at=time_now, last_login_at=time_now)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Функція для отримання користувача за його ID
async def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


async def get_all_users(db: Session):
    return db.query(models.User).all()

# Функція для створення початкових балів користувача
async def create_user_score(db: Session, user_id: int):
    user = await get_user(db, user_id)
    user_id = user.id
    scores = models.UserScore(user_id=user_id, score=0)
    db.add(scores)
    db.commit()
    db.refresh(scores)
    return scores


# Функція для отримання балів користувача за його ID
async def get_user_scores(db: Session, user_id: int):
    return db.query(models.UserScore).filter(models.UserScore.user_id == user_id).first()


# Функція для додавання балів користувачу
async def add_point(db: Session, count: int, user_id: int):
    user = await get_user(db, user_id)
    user_id = user.id
    score_user = get_user_scores(db, user_id)
    score_user.score += count
    db.add(score_user)
    db.commit()
    db.refresh(score_user)
    return score_user


# Функція для створення підсилення для користувача
async def create_user_boost(db: Session, user_id: int):
    user = await get_user(db, user_id)
    user_id = user.id
    boosts = models.Boosts(user_id=user_id, fill_char_count=1, charge_count=1, mine_coint=1)
    db.add(boosts)
    db.commit()
    db.refresh(boosts)
    return boosts


# Функція для отримання підсилення користувача за його ID
async def get_user_boosts(db: Session, user_id: int):
    return db.query(models.Boosts).filter(models.Boosts.user_id == user_id).first()


# Функція для зменшення заряду підсилення у користувача
async def dev_charge(db: Session, user_id: int):
    boosts = await get_user_boosts(db, user_id)
    count_miner = boosts.mine_coint
    boosts.charge_count -= count_miner
    db.commit()
    return boosts.charge_count


# Функція для створення зображення
async def create_image(db: Session, image_data: bytes):
    db_image = models.Image(data=image_data)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


# Функція для створення клану
async def create_clan(db: AsyncSession, clan: schemas.ClanCreate):
    # Створюємо новий об'єкт клану
    db_clan = models.Clan(**clan.dict())

    # Додаємо клан до сесії
    db.add(db_clan)

    # Зберігаємо зміни
    await db.commit()

    # Оновлюємо клан
    await db.refresh(db_clan)

    # Запит на отримання зображення
    stmt = select(models.Image).filter(models.Image.id == clan.img_id)
    result = await db.execute(stmt)
    db_image = result.scalars().first()

    # Додаємо зображення до клану, якщо знайдене
    if db_image:
        db_clan.image = db_image

    return db_clan


# Функція для отримання клану за його ID
async def get_clan(db: Session, clan_id: int):
    return db.query(models.Clan).filter(models.Clan.id == clan_id).first()


# Функція для створення початкових балів клану
async def create_clan_score(db: Session, clan_id: int):
    clan = await get_clan(db, clan_id)
    clan_id = clan.id
    scores = models.ClanScore(clan_id=clan_id, score=0)
    db.add(scores)
    db.commit()
    db.refresh(scores)
    return scores


# Функція для отримання балів клану за його ID
async def get_clan_scores(db: Session, clan_id: int):
    return db.query(models.ClanScore).filter(models.ClanScore.clan_id == clan_id).first()


# Функція для додавання балів клану
async def add_clan_point(db: Session, clan_id: int):
    clan = await get_clan(db, clan_id)
    clan_id = clan.id
    score_clan = await get_clan_scores(db, clan_id)
    score_clan.score += 1
    db.add(score_clan)
    db.commit()
    db.refresh(score_clan)
    return score_clan


# Функція для приєднання користувача до клану
async def enter_in_clan(db: Session, clan_id: int, user_id: int):
    db_clan_enter = models.UsersClan(user_id=user_id, clan_id=clan_id)
    db.add(db_clan_enter)
    db.commit()
    db.refresh(db_clan_enter)
    return db_clan_enter


# Функція для отримання клану користувача за його ID
# async def get_clans_for_user(db: Session, user_id: int):
#     return db.query(models.Clan).join(models.UsersClan).filter(models.UsersClan.user_id == user_id).first()

async def get_clans_for_user(db: Session, user_id: int):
    return db.query(models.Clan).join(models.UsersClan).filter(models.UsersClan.user_id == user_id).options(
        joinedload(models.Clan.count_score)
    ).first()


# Функція для виходу користувача з клану
async def leave_from_clan(db: Session, user_id: int):
    user_clan_record = db.query(models.UsersClan).filter(models.UsersClan.user_id == user_id).first()
    if user_clan_record:
        db.delete(user_clan_record)
        db.commit()
        return {"msg": "The user has left the clan"}
    else:
        return None


# async def get_all_clan(db: Session):
#     return db.query(models.Clan).all()

async def get_clans(db: Session):
    return db.query(models.Clan).join(models.UsersClan).options(joinedload(models.Clan.count_score)).all()


async def get_image(db: Session, image_id: int):
    return db.query(models.Image).filter(models.Image.id == image_id).first()


async def get_clan_members(db: Session, clan_id: int):
    return db.query(models.User).join(models.UsersClan).filter(models.UsersClan.clan_id == clan_id).options(joinedload(models.User.scores)).all()


async def get_leader_users(db: Session):
    return (db.query(models.User).join(models.UserScore, models.User.id == models.UserScore.user_id).order_by(models.UserScore.score.desc()).options(joinedload(models.User.scores)).all())


async def get_leader_clans(db: Session):
    return (db.query(models.Clan).join(models.ClanScore, models.Clan.id == models.ClanScore.clan_id).order_by(models.ClanScore.score.desc()).options(joinedload(models.Clan.count_score)).all())


async def div_points(db: Session, user_id: int, price: int):
    points = await get_user_scores(db, user_id)
    points.score -= price
    db.commit()
    return points.score


async def buy_fill_char(db: Session, user_id: int):
    bosts = await get_user_boosts(db, user_id)
    fillchar = bosts.fill_char_count
    if fillchar < 3:
        bosts.fill_char_count += 1
        db.commit()
        return bosts.fill_char_count


async def buy_charge_count(db: Session, user_id: int):
    bosts = await get_user_boosts(db, user_id)
    charge = bosts.charge_count
    if charge < 3:
        bosts.charge_count += 1
        db.commit()
        return bosts.charge_count


async def buy_mine_coint(db: Session, user_id: int):
    bosts = await get_user_boosts(db, user_id)
    mine_c = bosts.mine_coint
    if mine_c < 3:
        bosts.mine_coint += 1
        db.commit()
        return bosts.mine_coint


async def create_user_achivments(db: Session, user_id: int):
    user = await get_user(db, user_id)
    user_id = user.id
    achivments = models.UserAchivments(user_id=user_id, up_50k=0, up_100k=0, up_500k=0, up_1million=0)
    db.add(achivments)
    db.commit()
    db.refresh(achivments)
    return achivments


async def get_user_achivments(db: Session, user_id: int):
    return db.query(models.UserAchivments).filter(models.UserAchivments.user_id == user_id).first()


async def create_user_charge(db: Session, user_id: int):
    user = await get_user(db, user_id)
    user_id = user.id
    charge = models.UserCharges(user_id=user_id, charge=5000)
    db.add(charge)
    db.commit()
    db.refresh(charge)
    return charge


async def get_user_charge(db: Session, user_id: int):
    return db.query(models.UserCharges).filter(models.UserCharges.user_id == user_id).first()

async def add_charge_point(db: Session, user_id: int, points: int):
    charge = await get_user_charge(db, user_id)
    charge_c = charge.charge + points
    db.add(charge_c)
    db.commit()
    db.refresh(charge_c)
    return charge.charge


async def div_charge_point(db: Session, user_id: int, points: int):
    charge = await get_user_charge(db, user_id)
    charge_c = charge.charge - points
    db.add(charge_c)
    db.commit()
    db.refresh(charge_c)
    return charge.charge