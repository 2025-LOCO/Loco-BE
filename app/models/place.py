from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class PlaceType(str):
    # 필요 시 Enum으로 엄격화 가능. 우선 문자열 저장으로 둡니다.
    pass

class Place(Base):
    __tablename__ = "places"

    place_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    type: Mapped[str] = mapped_column(String(50))  # enum 문자열로 보관
    is_frequent: Mapped[bool] = mapped_column(Boolean, default=False)  # 자주가는/직접추가 구분
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    atmosphere: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    pros: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    cons: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    count_real: Mapped[int] = mapped_column(Integer, default=0)
    count_normal: Mapped[int] = mapped_column(Integer, default=0)
    count_bad: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # 위치 관련 추가 칼럼(필요 시 활성화)
    # lat: Mapped[Optional[float]] = mapped_column(nullable=True)
    # lng: Mapped[Optional[float]] = mapped_column(nullable=True)

    creator = relationship("User", back_populates="created_places")
    favorites = relationship("FavoritePlace", back_populates="place", cascade="all, delete-orphan")
    votes = relationship("PlaceVote", back_populates="place", cascade="all, delete-orphan")
    route_maps = relationship("RoutePlaceMap", back_populates="place", cascade="all, delete-orphan")