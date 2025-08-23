# app/schemas/route.py
from typing import Optional
from pydantic import BaseModel, Field

class RouteCreate(BaseModel):
    name: str = Field(..., max_length=255)
    is_recommend: bool = False
    image_url: Optional[str] = None
    tag_period: Optional[int] = None
    tag_env: Optional[str] = None
    tag_with: Optional[str] = None
    tag_move: Optional[str] = None
    tag_atmosphere: Optional[str] = None
    tag_place_count: Optional[int] = None

class RouteOut(BaseModel):
    route_id: int
    name: str
    is_recommend: bool
    image_url: Optional[str]
    count_real: int
    count_normal: int
    count_bad: int
    tag_period: Optional[int]
    tag_env: Optional[str]
    tag_with: Optional[str]
    tag_move: Optional[str]
    tag_atmosphere: Optional[str]
    tag_place_count: Optional[int]

    class Config:
        from_attributes = True