from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Loco(Base):
    __tablename__ = "locos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    specialties = Column(Text, nullable=True)  # 전문 분야 (JSON 형태)
    rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)
    hourly_rate = Column(Integer, nullable=True)  # 시간당 요금
    is_verified = Column(Boolean, default=False)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 관계 설정
    user = relationship("User", back_populates="loco_profile")
    region = relationship("Region")