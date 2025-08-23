from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from app.core.database import Base

# 담은 장소 (User <-> Place) + 추가 속성
class FavoritePlace(Base):
    __tablename__ = "favorite_places"
    __table_args__ = (
        UniqueConstraint("user_id", "place_id", name="uq_favorite_place_user_place"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    place_id: Mapped[int] = mapped_column(ForeignKey("places.place_id"), nullable=False, index=True)

    saved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_certificated: Mapped[bool] = mapped_column(Boolean, default=False)
    certificate_img_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)

    user = relationship("User", back_populates="favorite_places")
    place = relationship("Place", back_populates="favorites")


# 담은 루트 (User <-> Route)
class FavoriteRoute(Base):
    __tablename__ = "favorite_routes"
    __table_args__ = (
        UniqueConstraint("user_id", "route_id", name="uq_favorite_route_user_route"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    route_id: Mapped[int] = mapped_column(ForeignKey("routes.route_id"), nullable=False, index=True)

    saved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="favorite_routes")
    route = relationship("Route", back_populates="favorites")


# 루트-장소 매핑 (순서/이동수단 포함)
class RoutePlaceMap(Base):
    __tablename__ = "route_place_maps"
    __table_args__ = (
        UniqueConstraint("route_id", "place_id", "order", name="uq_route_place_order"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    route_id: Mapped[int] = mapped_column(ForeignKey("routes.route_id"), nullable=False, index=True)
    place_id: Mapped[int] = mapped_column(ForeignKey("places.place_id"), nullable=False, index=True)

    order: Mapped[int] = mapped_column()  # 루트 내 순서
    is_transportation: Mapped[bool] = mapped_column(default=False)
    transportation_name: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    route = relationship("Route", back_populates="places")
    place = relationship("Place", back_populates="route_maps")