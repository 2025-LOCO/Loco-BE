# app/schemas/route.py
from typing import Optional, List
from pydantic import BaseModel, Field

class HashTag(BaseModel):
    period: Optional[int] = None
    env: Optional[str] = None
    with_whom: Optional[str] = None
    move: Optional[str] = None
    atmosphere: Optional[str] = None
    place_count: Optional[int] = None

class RoutePlace(BaseModel):
    place_id: int
    name: str
    image_url: Optional[str] = None
    latitude: float
    longitude: float

class Transportation(BaseModel):
    name: str
    # 필요하다면 여기에 더 많은 필드를 추가할 수 있습니다.

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
    user_id: int
    city_name: Optional[str] = None
    liked: int
    tags: HashTag
    places: List[RoutePlace]
    transportations: List[Transportation]

    class Config:
        from_attributes = True

class RouteExploreOut(BaseModel):
    ranked_routes: List[RouteOut]
    new_routes: List[RouteOut]