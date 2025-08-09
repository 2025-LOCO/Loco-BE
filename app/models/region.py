from sqlalchemy import Column, Integer, String, Boolean, Float
from app.core.database import Base


class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)  # SGIS 지역코드
    name = Column(String, nullable=False)
    kor_name = Column(String, nullable=False)
    parent_code = Column(String, nullable=True)  # 상위 지역 코드
    level = Column(Integer, nullable=False)  # 1: 시도, 2: 시군구, 3: 읍면동
    x_coord = Column(Float, nullable=True)
    y_coord = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)