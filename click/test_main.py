import pytest
from httpx import AsyncClient
from fastapi import status
from main import app  # Import your FastAPI app

# Mocking the dependencies
from database.database import get_db_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db():
    # Create the database and tables
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    # Drop the tables
    models.Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db_session] = override_get_db

@pytest.mark.asyncio
async def test_root(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient, db):
    user_data = {"username": "testuser", "password": "testpass"}
    response = await client.post("/create_user", json=user_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "testuser"

@pytest.mark.asyncio
async def test_get_user(client: AsyncClient, db):
    user_id = 1
    response = await client.get(f"/get_user?id={user_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == user_id

@pytest.mark.asyncio
async def test_get_all_users(client: AsyncClient, db):
    response = await client.get("/get_all_users")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_create_user_scores(client: AsyncClient, db):
    user_id = 1
    response = await client.post(f"/create_user_scores?user_id={user_id}")
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_add_user_scores(client: AsyncClient, db):
    user_id = 1
    count = 10
    response = await client.post(f"/add_user_scores?user_id={user_id}&count={count}")
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_create_user_boosts(client: AsyncClient, db):
    user_id = 1
    response = await client.post(f"/create_user_boosts?user_id={user_id}")
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_get_user_boosts(client: AsyncClient, db):
    user_id = 1
    response = await client.get(f"/get_user_boosts?user_id={user_id}")
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_create_clan(client: AsyncClient, db):
    clan_data = {"name": "Test Clan", "img_id": 1}
    response = await client.post("/clans/", json=clan_data)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_read_clan(client: AsyncClient, db):
    clan_id = 1
    response = await client.get(f"/clans/{clan_id}")
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_upload_file(client: AsyncClient, db):
    file_data = {'file': ('filename', b'file_content', 'image/png')}
    response = await client.post("/uploadfile/", files=file_data)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_enter_in_clan(client: AsyncClient, db):
    user_id = 1
    clan_id = 1
    response = await client.post(f"/enter_in_clan?user_id={user_id}&clan_id={clan_id}")
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_get_user_clan(client: AsyncClient, db):
    user_id = 1
    response = await client.get(f"/get_user_clan?user_id={user_id}")
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_leave_from_clan(client: AsyncClient, db):
    user_id = 1
    response = await client.delete(f"/leave_from_clan?user_id={user_id}")
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_add_point_clan(client: AsyncClient, db):
    clan_id = 1
    response = await client.post(f"/add_point_clan?clan_id={clan_id}")
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_get_all_clans(client: AsyncClient, db):
    response = await client.get("/get_all_clans")
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_read_image(client: AsyncClient, db):
    image_id = 1
    response = await client.get(f"/images/{image_id}")
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_get_clan_member(client: AsyncClient, db):
    clan_id = 1
    response = await client.get(f"/clan_members?clan_id={clan_id}")
    assert response.status_code == status.HTTP_200_OK
