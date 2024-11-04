from datetime import datetime
from .testconfig import ac
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_user(ac: AsyncClient):
    response = await ac.post("/create_user", json={
        "name": "testuser",
        "tg_id": 123,
        "register_at": f"{datetime.now()}",
        "last_login_at": f"{datetime.now()}",
        "scores": {
            "score": 0
        },
        "charges": {
            "charge": 5000
        }
    })
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_clan(ac: AsyncClient):
    response = await ac.post("/uploadfile/", files={"file": ("test.png", b"image data", "image/png")})
    assert response.status_code == 200
    image_id = response.json()["image_id"]

    response = await ac.post("/clans/", json={"name": "testclan", "img_id": image_id})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_enter_in_clan(ac: AsyncClient):
    response = await ac.post("/enter_in_clan", json={"user_id": 1, "clan_id": 1})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_leaderboard_user(ac: AsyncClient):
    response = await ac.get("/get_leaderboard_user")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_add_user_scores(ac: AsyncClient):
    response = await ac.post("/add_user_scores", json={"user_id": 1, "count": 50})
    assert response.status_code == 200
