# app/schemas/route.py
from typing import Optional, List
from pydantic import BaseModel, Field

class RoutePlaceCreate(BaseModel):
    place_id: int
    day: int
    order: int

class TransportationCreate(BaseModel):
    name: str
    day: int
    order: int

class RouteCreate(BaseModel):
    name: str
    is_recommend: bool = False
    image_url: Optional[str] = None
    tag_period: Optional[int] = None
    tag_env: Optional[str] = None
    tag_with: Optional[str] = None
    tag_move: Optional[str] = None
    tag_atmosphere: Optional[str] = None
    tag_place_count: Optional[int] = None
    places: List[RoutePlaceCreate]
    transportations: List[TransportationCreate]

    class Config:
        from_attributes = True

class HashTag(BaseModel):
    period: str         # 여행 기간 (ex. "1박2일")
    env: str            # 장소 환경 (ex. "도시" / "자연")
    with_who: str = Field(..., alias='with')           # 동반자 (ex. "연인")
    move: str           # 이동수단 (ex. "자동차")
    atmosphere: str     # 분위기 (ex. "잔잔하고 조용한")
    place_count: str    # 하루 방문지 수 (ex. "3")

class RoutePlace(BaseModel):
    id: int
    name: str
    category: str
    day: int
    order: int

class Transportation(BaseModel):
    id: int
    name: str
    day: int
    order: int

class LocoRoute(BaseModel):
    user_id: Optional[int] = Field(None, alias='userId')
    id: int
    name: str
    image_url: Optional[str] = Field(None, alias='imageUrl')
    location: Optional[str] = None
    intro: Optional[str] = None
    liked: int
    tags: HashTag
    places: List[RoutePlace]
    transportations: List[Transportation]
    count_real: Optional[int] = Field(None, alias='countReal')
    count_soso: Optional[int] = Field(None, alias='countSoso')
    count_bad: Optional[int] = Field(None, alias='countBad')

    class Config:
        from_attributes = True
        populate_by_name = True


class RouteOut(BaseModel):
    route_id: int = Field(..., alias='routeId')
    name: str
    is_recommend: bool = Field(..., alias='isRecommend')
    image_url: Optional[str] = Field(None, alias='imageUrl')
    count_real: int = Field(..., alias='countReal')
    count_soso: int = Field(..., alias='countSoso')
    count_bad: int = Field(..., alias='countBad')
    user_id: int = Field(..., alias='userId')
    city_name: Optional[str] = Field(None, alias='cityName')
    liked: int
    tags: HashTag
    places: List[RoutePlace]
    transportations: List[Transportation]

    class Config:
        from_attributes = True
        populate_by_name = True

class RouteExploreOut(BaseModel):
    ranked_routes: List[LocoRoute]
    new_routes: List[LocoRoute]

    class Config:
        populate_by_name = True