from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base
from pgvector.sqlalchemy import Vector


class Route(Base):
    __tablename__ = "routes"

    route_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    intro: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_recommend: Mapped[bool] = mapped_column(Boolean, default=False)  # 추천/직접만든 구분
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    count_real: Mapped[int] = mapped_column(Integer, default=0)
    count_soso: Mapped[int] = mapped_column(Integer, default=0)
    count_bad: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.current_timestamp())

    # 태그들
    tag_period: Mapped[Optional[int]] = mapped_column(nullable=True)                # 1~33 (32 장기, 33 all)
    tag_env: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)       # sea/mountain/city/country/all
    tag_with: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)      # alone/friend/family/pet/love/all
    tag_move: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)      # walk/bicycle/car/public/train/all
    tag_atmosphere: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    tag_place_count: Mapped[Optional[int]] = mapped_column(nullable=True)           # 1~6 (6 all)

    creator = relationship("User", back_populates="created_routes")
    favorites = relationship("FavoriteRoute", back_populates="route", cascade="all, delete-orphan")
    votes = relationship("RouteVote", back_populates="route", cascade="all, delete-orphan")
    places = relationship("RoutePlaceMap", back_populates="route", cascade="all, delete-orphan")

    # 해시태그 벡터를 저장할 컬럼
    embedding: Mapped[Vector] = mapped_column(Vector(768), nullable=True)