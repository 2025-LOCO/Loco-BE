from pydantic import BaseModel
from typing import Optional


class RegionBase(BaseModel):
    code: str
    name: str
    kor_name: str
    parent_code: Optional[str] = None
    level: int
    x_coord: Optional[float] = None
    y_coord: Optional[float] = None


class RegionCreate(RegionBase):
    pass


class Region(RegionBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True