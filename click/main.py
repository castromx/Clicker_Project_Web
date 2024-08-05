from fastapi import FastAPI, status, Depends, HTTPException, UploadFile, File
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from database import schemas, models, crud
from sqlalchemy.orm import Session
from database.database import get_async_session
from task_router import router
app = FastAPI()
app.include_router(router)
from sqlalchemy.future import select
@app.get("/")
async def root():
    return status.HTTP_200_OK



origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/create_user")
async def create_user(user: schemas.UserAccount, db: Session = Depends(get_async_session)) -> schemas.UserAccount:
    user = await crud.create_user(db=db, user=user)
    await crud.create_user_score(db, user.id)
    await crud.create_user_boost(db, user.id)
    await crud.create_user_achivments(db, user.id)
    await crud.create_user_charge(db, user.id)
    return user


@app.get("/get_user")
async def get_user(id: int, db: Session = Depends(get_async_session)) -> schemas.UserAccount:
    return await crud.get_user(db, id)


@app.get("/get_all_users")
async def get_all_users(db: Session = Depends(get_async_session)):
    return crud.get_all_users(db)


@app.get("/get_user_score")
async def get_user_score(user_id: int, db: Session = Depends(get_async_session)):
    return crud.get_user_scores(db, user_id)


@app.post("/create_user_scores")
async def create_user_scores(user_id: int, db: Session = Depends(get_async_session)):
    return crud.create_user_score(db, user_id)


@app.post("/add_user_scores")
async def add_user_scores(user_id: int, count: int, db: Session = Depends(get_async_session)):
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
    elif charge < 1:
        return "Energy charge too low"


@app.post("/create_user_boosts")
async def create_user_boosts(user_id: int, db: Session = Depends(get_async_session)):
    return crud.create_user_boost(db, user_id)


@app.get("/get_user_boosts")
async def get_user_boosts(user_id: int, db: Session = Depends(get_async_session)):
    boosts = crud.get_user_boosts(db, user_id)
    return boosts


@app.post("/clans/", response_model=schemas.Clan)
async def create_clan(clan: schemas.ClanCreate, db: Session = Depends(get_async_session)):
    # Перевірка наявності зображення
    stmt = select(models.Image).filter(models.Image.id == clan.img_id)
    result = await db.execute(stmt)
    db_image = result.scalars().first()

    if not db_image:
        raise HTTPException(status_code=422, detail="Image not found")

    # Створення клану
    db_clan = await crud.create_clan(db=db, clan=clan)
    await crud.create_clan_score(db, db_clan.id)

    return db_clan



@app.get("/clans/{clan_id}", response_model=schemas.Clan)
async def read_clan(clan_id: int, db: Session = Depends(get_async_session)):
    db_clan = await crud.get_clan(db=db, clan_id=clan_id)
    if db_clan is None:
        raise HTTPException(status_code=404, detail="Clan not found")
    return db_clan


@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_async_session)):
    file_data = file.file.read()
    db_image = await crud.create_image(db=db, image_data=file_data)
    return {"image_id": db_image.id}


@app.post("/enter_in_clan")
async def enter_in_clan(user_id: int, clan_id: int, db: Session = Depends(get_async_session)):
    if await crud.get_clans_for_user(db, user_id):
        raise HTTPException(status_code=422, detail="Вам потрібно вийти з попереднього клану, щоб приєднатись у цей")
    return crud.enter_in_clan(db, clan_id, user_id)


@app.get("/get_user_clan")
async def get_user_clan(user_id: int, db: Session = Depends(get_async_session)):
    return crud.get_clans_for_user(db, user_id)


@app.delete("/leave_from_clan")
async def leave_from_clan(user_id: int, db: Session = Depends(get_async_session)):
    result = crud.leave_from_clan(db, user_id)
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="The user was not in a clan")


@app.post("/add_point_clan")
async def add_point_clan(clan_id: int, db: Session = Depends(get_async_session)):
    return crud.add_clan_point(db, clan_id)


@app.get('/get_all_clans')
async def get_all_clans(db: Session = Depends(get_async_session)):
    return crud.get_clans(db)


@app.get("/images/{image_id}")
async def read_image(image_id: int, db: Session = Depends(get_async_session)):
    db_image = await crud.get_image(db, image_id=image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")

    temp_file_path = f"temp_image_{image_id}.png"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(db_image.data)

    return FileResponse(temp_file_path, media_type='image/png', filename=f"image_{image_id}.png")


@app.get("/clan_members")
async def get_clan_member(clan_id: int, db: Session = Depends(get_async_session)):
    return crud.get_clan_members(db, clan_id)


@app.get("/get_leaderboard_user")
async def get_leaderboard_user(db: Session = Depends(get_async_session)):
    return crud.get_leader_users(db)


@app.get("/get_leaderboard_clan")
async def get_leaderboard_clan(db: Session = Depends(get_async_session)):
    return crud.get_leader_clans(db)


@app.post("/div_point")
async def div_user_point(user_id: int, price: int, db: Session = Depends(get_async_session)):
    point = await crud.get_user_scores(db, user_id)
    point = point.score
    if point > price:
        return crud.div_points(db, user_id, price)
    return HTTPException(status_code=422, detail="You have not enough points")


@app.post("/buy_fill_char_count")
async def buy_fill_char(user_id: int, db: Session = Depends(get_async_session)):
    point = await crud.get_user_scores(db, user_id)
    point = point.score
    price = point * 10
    if point > price:
        await crud.div_points(db, user_id, price)
        return crud.buy_fill_char(db, user_id)
    return HTTPException(status_code=422, detail="You have not enough points")


@app.post("/buy_charge_count")
async def buy_charge(user_id: int, db: Session = Depends(get_async_session)):
    point = await crud.get_user_scores(db, user_id)
    point = point.score
    price = point * 10
    if point > price:
        await crud.div_points(db, user_id, price)
        return crud.buy_charge_count(db, user_id)
    return HTTPException(status_code=422, detail="You have not enough points")


@app.post("/buy_mine_coint")
async def buy_mine(user_id: int, db: Session = Depends(get_async_session)):
    point = await crud.get_user_scores(db, user_id)
    point = point.score
    price = point * 10
    if point > price:
        await crud.div_points(db, user_id, price)
        return crud.buy_mine_coint(db, user_id)
    return HTTPException(status_code=422, detail="You have not enough points")


@app.get("/get_user_achivments", response_model=schemas.Achivments)
async def get_user_achivments(user_id: int, db: Session = Depends(get_async_session)):
    return crud.get_user_achivments(db, user_id)

@app.post("/fill_charge_count")
async def fill_charge(user_id: int, point: int, db: Session = Depends(get_async_session)):
    boosts = await crud.get_user_boosts(db, user_id)
    charge_lvl = boosts.charge_count
    charge = await crud.get_user_charge(db, user_id)
    max_charge = charge_lvl * 5000
    if charge < max_charge:
        await crud.add_charge_point(db, user_id, point)
    return {"fill": "full"}


@app.post("/div_point")
async def div_user_point(user_id: int, db: Session = Depends(get_async_session)):
    return crud.div_charge_point(db, user_id, 1)


