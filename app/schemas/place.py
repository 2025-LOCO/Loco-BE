# app/schemas/place.py
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator

class PlaceCreate(BaseModel):
    name: str = Field(..., max_length=255)
    type: str = Field(..., max_length=50)
    is_frequent: bool = False
    atmosphere: Optional[str] = Field(None, max_length=20)
    pros: Optional[str] = Field(None, max_length=100)
    cons: Optional[str] = Field(None, max_length=100)
    image_url: Optional[str] = None
    latitude: float
    longitude: float
    kakao_place_id: Optional[str] = Field(None, max_length=64)
    intro: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    address_name: Optional[str] = Field(None, max_length=255)
    short_location: Optional[str] = Field(None, max_length=100)
    link: Optional[str] = Field(None, max_length=255)

class PlaceOut(BaseModel):
    place_id: int
    name: str
    type: str
    is_frequent: bool
    atmosphere: Optional[str]
    pros: Optional[str]
    cons: Optional[str]
    image_url: Optional[str]
    count_real: int
    count_normal: int
    count_bad: int
    latitude: float
    longitude: float
    kakao_place_id: Optional[str] = None
    intro: Optional[str] = None
    phone: Optional[str] = None
    address_name: Optional[str] = None
    link: Optional[str] = None
    liked: int
    user_id: int
    city_name: Optional[str] = None

    class Config:
        from_attributes = True


class PlaceBase(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    is_frequent: Optional[bool] = None
    atmosphere: Optional[str] = None
    pros: Optional[str] = None
    cons: Optional[str] = None
    image_url: Optional[str] = None
    kakao_place_id: Optional[str] = None


class PlaceSearchResult(BaseModel):
    member_id: int
    place_id: int
    name: str
    image_url: Optional[str] = None
    liked: int
    short_location: Optional[str] = None
    intro: Optional[str] = None

class PlaceExploreOut(BaseModel):
    ranked_places: List[PlaceSearchResult]
    new_places: List[PlaceSearchResult]