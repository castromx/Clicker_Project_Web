from datetime import datetime
from pydantic import BaseModel


class UserCharges(BaseModel):
    charge: int  # Кількість балів користувача

    class Config:
        from_attributes = True

class UserScores(BaseModel):
    score: int  # Кількість балів користувача

    class Config:
        from_attributes = True


class UserAccount(BaseModel):
    name: str  # Ім'я користувача
    tg_id: int  # Telegram ID користувача
    register_at: datetime  # Дата реєстрації користувача
    last_login_at: datetime  # Дата останнього входу користувача
    scores: UserScores
    charges: UserCharges
    clan: ClanCreate

    class Config:
        from_attributes = True


class ClanScores(BaseModel):
    score: int  # Кількість балів клану

    class Config:
        from_attributes = True


class Boosts(BaseModel):
    user_id: int  # ID користувача
    fill_char_count: int  # Кількість заповнених символів
    charge_count: int  # Кількість зарядів
    mine_coint: int  # Кількість монет, здобутих при майнінгу

    class Config:
        from_attributes = True


class MainPage(BaseModel):
    user: UserAccount  # Обліковий запис користувача
    user_scores: UserScores  # Бали користувача
    boosts: Boosts  # Підсилення користувача

    class Config:
        from_attributes = True


# Модель для створення клану
class ClanCreate(BaseModel):
    name: str  # Назва клану
    img_id: int  # ID зображення клану


class Clan(BaseModel):
    id: int  # ID клану
    name: str  # Назва клану
    count_score: ClanScores  # Кількість балів клану
    img_id: int  # ID зображення клану

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Example Clan",
                "img_id": 123,
                "count_score": {
                    "clan_id": 1,
                    "score": 1000
                }
            }
        }


class ImageBase(BaseModel):
    id: int
    data: bytes


class Image(ImageBase):
    class Config:
        from_attributes = True


class Achivments(BaseModel):
    id: int
    up_100k: bool
    up_1million: bool
    up_50k: bool
    up_500k: bool
