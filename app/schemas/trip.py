from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TripBase(BaseModel):
    title: str
    description: Optional[str] = None
    region_id: int
    sub_region_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_public: bool = True


class TripCreate(TripBase):
    pass


class TripUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_public: Optional[bool] = None


class Trip(TripBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True