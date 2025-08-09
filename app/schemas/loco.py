from pydantic import BaseModel
from typing import Optional


class LocoBase(BaseModel):
    region_id: int
    specialties: Optional[str] = None
    hourly_rate: Optional[int] = None


class LocoCreate(LocoBase):
    pass


class LocoUpdate(BaseModel):
    specialties: Optional[str] = None
    hourly_rate: Optional[int] = None
    is_available: Optional[bool] = None


class Loco(LocoBase):
    id: int
    user_id: int
    rating: float
    review_count: int
    is_verified: bool
    is_available: bool

    class Config:
        from_attributes = True