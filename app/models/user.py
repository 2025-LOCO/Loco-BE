# app/models/user.py
from typing import Optional
from datetime import datetime
from xmlrpc.client import Boolean

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy import Boolean

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # 토큰 버전 (로그아웃/세션 무효화를 위한 전역 카운터)
    token_version: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # 인증용
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # 프로필
    nickname: Mapped[str] = mapped_column(String(10), unique=True, index=True)
    intro: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    city_id: Mapped[Optional[str]] = mapped_column(ForeignKey("region_cities.region_id"), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    city = relationship("RegionCity", back_populates="users")

    created_places = relationship("Place", back_populates="creator", cascade="all, delete-orphan", passive_deletes=True)
    created_routes = relationship("Route", back_populates="creator", passive_deletes=True)

    favorite_places = relationship("FavoritePlace", back_populates="user", cascade="all, delete-orphan")
    favorite_routes = relationship("FavoriteRoute", back_populates="user", cascade="all, delete-orphan")

    place_votes = relationship("PlaceVote", back_populates="user", cascade="all, delete-orphan")
    route_votes = relationship("RouteVote", back_populates="user", cascade="all, delete-orphan")

    questions = relationship("Question", back_populates="author", cascade="all, delete-orphan")
    answers = relationship("Answer", back_populates="author", cascade="all, delete-orphan")

    # 현지인 여부 추가
    city_id: Mapped[Optional[str]] = mapped_column(ForeignKey("region_cities.region_id"), nullable=True)
    is_local: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
