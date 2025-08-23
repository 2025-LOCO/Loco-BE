from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from app.core.database import Base

class RegionCity(Base):
    __tablename__ = "region_cities"

    region_id: Mapped[str] = mapped_column(String(6), primary_key=True)  # 시/군 코드
    province_id: Mapped[str] = mapped_column(ForeignKey("region_provinces.province_id"), nullable=False)
    kor_name: Mapped[str] = mapped_column(String(10))
    eng_name: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    province = relationship("RegionProvince", back_populates="cities")
    users = relationship("User", back_populates="city")  # User.city_id FK 대상