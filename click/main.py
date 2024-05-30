import aioredis
from fastapi import FastAPI, status, Depends, HTTPException, UploadFile, File
from starlette.middleware.cors import CORSMiddleware

from database import schemas, models, crud
from sqlalchemy.orm import Session
from database.database import get_db_session

app = FastAPI()

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
async def create_user(user: schemas.UserAccount, db: Session = Depends(get_db_session)) -> schemas.UserAccount:
    user = crud.create_user(db=db, user=user)
    crud.create_user_score(db, user.id)
    crud.create_user_boost(db, user.id)
    return user


@app.get("/get_user")
async def get_user(id: int, db: Session = Depends(get_db_session)) -> schemas.UserAccount:
    return crud.get_user(db, id)


@app.get("/get_user_score")
async def get_user_score(user_id: int, db: Session = Depends(get_db_session)):
    return crud.get_user_scores(db, user_id)


@app.post("/create_user_scores")
async def create_user_scores(user_id: int, db: Session = Depends(get_db_session)):
    return crud.create_user_score(db, user_id)


@app.post("/add_user_scores")
async def add_user_scores(user_id: int, count: int, db: Session = Depends(get_db_session)):
    boosts = crud.get_user_boosts(db, user_id)
    charge = boosts.charge_count * 600
    count = boosts.mine_coint * count
    if charge > 1:
        crud.add_point(db, count, user_id)
        crud.dev_charge(db, user_id)
        charge_after = boosts.charge_count
        count_after = crud.get_user_scores(db, user_id)
        return {"charge": charge_after, "count": count_after.score}
    elif charge < 1:
        return "Energy charge too low"


@app.post("/create_user_boosts")
async def create_user_boosts(user_id: int, db: Session = Depends(get_db_session)):
    return crud.create_user_boost(db, user_id)

@app.get("/get_user_boosts")
async def get_user_boosts(user_id: int, db: Session = Depends(get_db_session)):
    boosts = crud.get_user_boosts(db, user_id)
    return boosts

@app.post("/clans/", response_model=schemas.Clan)
def create_clan(clan: schemas.ClanCreate, db: Session = Depends(get_db_session)):
    return crud.create_clan(db=db, clan=clan)

# URL для отримання конкретного клану за ідентифікатором
@app.get("/clans/{clan_id}", response_model=schemas.Clan)
def read_clan(clan_id: int, db: Session = Depends(get_db_session)):
    db_clan = crud.get_clan(db=db, clan_id=clan_id)
    if db_clan is None:
        raise HTTPException(status_code=404, detail="Clan not found")
    return db_clan


# URL для завантаження фото
@app.post("/uploadfile/")
def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db_session)):
    # Отримуємо дані з файлу
    file_data = file.file.read()

    # Зберігаємо фото у базі даних
    db_image = crud.create_image(db=db, image_data=file_data)

    return {"image_id": db_image.id}
