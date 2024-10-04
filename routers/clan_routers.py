from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import schemas, crud, models
from ..database.database import get_async_session
from sqlalchemy.future import select


router = APIRouter()


@router.post("/clans/", response_model=schemas.Clan)
async def create_clan(clan: schemas.ClanCreate, db: AsyncSession = Depends(get_async_session)):
    stmt = select(models.Image).filter(models.Image.id == clan.img_id)
    result = await db.execute(stmt)
    db_image = result.scalars().first()

    if not db_image:
        raise HTTPException(status_code=422, detail="Image not found")
    db_clan = await crud.create_clan(db=db, clan=clan)
    await crud.create_clan_score(db, db_clan.id)

    return db_clan


@router.get("/clans/{clan_id}", response_model=schemas.Clan)
async def read_clan(clan_id: int, db: AsyncSession = Depends(get_async_session)):
    db_clan = await crud.get_clan(db=db, clan_id=clan_id)
    if db_clan is None:
        raise HTTPException(status_code=404, detail="Clan not found")
    return db_clan


@router.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...), db: AsyncSession = Depends(get_async_session)):
    file_data = file.file.read()
    db_image = await crud.create_image(db=db, image_data=file_data)
    return {"image_id": db_image.id}


@router.post("/enter_in_clan")
async def enter_in_clan(user_id: int, clan_id: int, db: AsyncSession = Depends(get_async_session)):
    if await crud.get_clans_for_user(db, user_id):
        raise HTTPException(status_code=422, detail="You need to leave the previous clan before joining this one")
    return await crud.enter_in_clan(db, clan_id, user_id)


@router.get("/get_user_clan")
async def get_user_clan(user_id: int, db: AsyncSession = Depends(get_async_session)):
    return await crud.get_clans_for_user(db, user_id)


@router.delete("/leave_from_clan")
async def leave_from_clan(user_id: int, db: AsyncSession = Depends(get_async_session)):
    result = await crud.leave_from_clan(db, user_id)
    if result:
        return result
    raise HTTPException(status_code=404, detail="The user was not in a clan")


@router.post("/add_point_clan")
async def add_point_clan(clan_id: int, db: AsyncSession = Depends(get_async_session)):
    return await crud.add_clan_point(db, clan_id)


@router.get('/get_all_clans')
async def get_all_clans(db: AsyncSession = Depends(get_async_session)):
    return await crud.get_clans(db)


@router.get("/images/{image_id}")
async def read_image(image_id: int, db: AsyncSession = Depends(get_async_session)):
    db_image = await crud.get_image(db, image_id=image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")

    temp_file_path = f"clan_photo/clan_image_{image_id}.png"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(db_image.data)

    return FileResponse(temp_file_path, media_type='image/png', filename=f"image_{image_id}.png")


@router.get("/clan_members")
async def get_clan_member(clan_id: int, db: AsyncSession = Depends(get_async_session)):
    return await crud.get_clan_members(db, clan_id)