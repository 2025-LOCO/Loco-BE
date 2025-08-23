from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class SurveySession(Base):
    """
    설문 1회 응답 저장. 익명 응답도 허용하려면 user_id를 Optional로 둡니다.
    """
    __tablename__ = "survey_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # 설문 답변 원문(정규화된 태그값으로 저장)
    period: Mapped[Optional[int]] = mapped_column(nullable=True)                 # 1~31, 32(한 달), 33(장기)
    env: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)        # sea/mountain/city/country
    with_whom: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # alone/friend/love/family/pet
    move: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)       # walk/bicycle/car/train/public
    atmosphere: Mapped[Optional[str]] = mapped_column(String(50), nullable=True) # 제안한 5가지 중 택1
    place_count: Mapped[Optional[int]] = mapped_column(nullable=True)            # 1~5

    user = relationship("User")  # 단방향 참조