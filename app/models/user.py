# app/models/user.py
from typing import Optional
from datetime import datetime
import enum

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Integer, String, DateTime, ForeignKey, Boolean,
    Enum as SQLAlchemyEnum
)
from sqlalchemy.sql import func
from app.core.database import Base


# 3. 'enum.Enum'을 사용하여 등급 클래스를 정의합니다.
class UserGrade(str, enum.Enum):
    S = "S"
    A = "A"
    B = "B"
    C = "C"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # 토큰 버전
    token_version: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # 인증용
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # 프로필
    nickname: Mapped[str] = mapped_column(String(10), unique=True, index=True)
    intro: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    city_id: Mapped[Optional[str]] = mapped_column(ForeignKey("region_cities.region_id"), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.current_timestamp())
    is_local: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # 랭킹, 포인트, 등급 컬럼
    ranking: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    grade: Mapped[UserGrade] = mapped_column(
        SQLAlchemyEnum(UserGrade),
        default=UserGrade.C,
        nullable=False
    )

    # --- 관계 설정 ---
    city = relationship("RegionCity", back_populates="users")
    created_places = relationship("Place", back_populates="creator", cascade="all, delete-orphan", passive_deletes=True)
    created_routes = relationship("Route", back_populates="creator", passive_deletes=True)
    favorite_places = relationship("FavoritePlace", back_populates="user", cascade="all, delete-orphan")
    favorite_routes = relationship("FavoriteRoute", back_populates="user", cascade="all, delete-orphan")
    place_votes = relationship("PlaceVote", back_populates="user", cascade="all, delete-orphan")
    route_votes = relationship("RouteVote", back_populates="user", cascade="all, delete-orphan")
    questions = relationship("Question", back_populates="author", cascade="all, delete-orphan")
    answers = relationship("Answer", back_populates="author", cascade="all, delete-orphan")