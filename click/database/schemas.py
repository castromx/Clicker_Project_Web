from datetime import datetime
from pydantic import BaseModel

# Модель для облікового запису користувача
class UserAccount(BaseModel):
    name: str  # Ім'я користувача
    tg_id: int  # Telegram ID користувача
    register_at: datetime  # Дата реєстрації користувача
    last_login_at: datetime  # Дата останнього входу користувача

    class Config:
        orm_mode = True

# Модель для збереження кількості балів користувача
class UserScores(BaseModel):
    score: int  # Кількість балів користувача

    class Config:
        orm_mode = True

# Модель для збереження кількості балів клану
class ClanScores(BaseModel):
    count_score: int  # Кількість балів клану

    class Config:
        orm_mode = True

# Модель для збереження інформації про підсилення користувача
class Boosts(BaseModel):
    user_id: int  # ID користувача
    fill_char_count: int  # Кількість заповнених символів
    charge_count: int  # Кількість зарядів
    mine_coint: int  # Кількість монет, здобутих при майнінгу

    class Config:
        orm_mode = True

# Модель для головної сторінки, яка включає інформацію про користувача, його бали та підсилення
class MainPage(BaseModel):
    user: UserAccount  # Обліковий запис користувача
    user_scores: UserScores  # Бали користувача
    boosts: Boosts  # Підсилення користувача

    class Config:
        orm_mode = True

# Модель для створення клану
class ClanCreate(BaseModel):
    name: str  # Назва клану
    img_id: int  # ID зображення клану

# Модель для представлення клану
class Clan(BaseModel):
    id: int  # ID клану
    name: str  # Назва клану
    img_id: int  # ID зображення клану

    class Config:
        orm_mode = True

# Модель для представлення зображення
class Image(BaseModel):
    id: int  # ID зображення
    data: bytes  # Дані зображення

    class Config:
        orm_mode = True
