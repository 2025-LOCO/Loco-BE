from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from app.core.database import Base

class RegionProvince(Base):
    __tablename__ = "region_provinces"

    province_id: Mapped[str] = mapped_column(String(2), primary_key=True)  # 시/도 코드
    kor_name: Mapped[str] = mapped_column(String(10))
    eng_name: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    # 하위 시/군 목록
    cities = relationship("RegionCity", back_populates="province", cascade="all, delete-orphan")