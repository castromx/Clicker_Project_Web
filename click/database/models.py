from datetime import datetime
from sqlalchemy import ForeignKey, LargeBinary, Integer
from sqlalchemy import String
from .database import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    tg_id: Mapped[int] = mapped_column(unique=True)
    scores: Mapped["ClanScore"] = relationship("UserScore", back_populates="user")
    clans: Mapped[int] = relationship("UsersClan", back_populates="user")
    boosts: Mapped[int] = relationship("Boosts", back_populates="user")
    achivments: Mapped[int] = relationship("UserAchivments", back_populates="user")
    register_at: Mapped[datetime]
    last_login_at: Mapped[datetime]


class Boosts(Base):
    __tablename__ = "boosts"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    fill_char_count: Mapped[int]  # заповнення заряду
    charge_count: Mapped[int]  # к-ть заряду
    mine_coint: Mapped[int]  # К-ть монет, видобутих за клік
    user: Mapped[User] = relationship("User", back_populates="boosts")

    def __repr__(self) -> str:
        return f"Boosts(id={self.id!r}, user_id={self.user_id!r})"


class UserScore(Base):
    __tablename__ = "user_score"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    score: Mapped[int]
    user: Mapped[User] = relationship("User", back_populates="scores")


class Image(Base):
    __tablename__ = "image"
    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[bytes] = mapped_column(LargeBinary)
    clans: Mapped[int] = relationship("Clan", back_populates="img")


class Clan(Base):
    __tablename__ = "clan"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    img_id: Mapped[int] = mapped_column(ForeignKey('image.id'))
    count_score: Mapped["ClanScore"] = relationship("ClanScore", back_populates="clan")
    img: Mapped["Image"] = relationship("Image", back_populates="clans")

class ClanScore(Base):
    __tablename__ = "clan_score"
    id: Mapped[int] = mapped_column(primary_key=True)
    clan_id: Mapped[int] = mapped_column(ForeignKey("clan.id"))
    score: Mapped[int] = mapped_column(Integer)
    clan: Mapped[Clan] = relationship("Clan", back_populates="count_score")



class UsersClan(Base):
    __tablename__ = "users_id_clan"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    clan_id: Mapped[int] = mapped_column(ForeignKey("clan.id"))
    user: Mapped[User] = relationship("User", back_populates="clans")

class UserAchivments(Base):
    __tablename__ = "user_achivments"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    up_50k: Mapped[bool]
    up_100k: Mapped[bool]
    up_500k: Mapped[bool]
    up_1million: Mapped[bool]
    user: Mapped[User] = relationship("User", back_populates="achivments")


class Charge(Base):
    __tablename__ = "charge"
    id: Mapped[int] = mapped_column(primary_key=True)
    charge: Mapped[int]
    user: Mapped[Boosts] = relationship("Boosts", back_populates="charge_count")
    
