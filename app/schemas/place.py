# app/schemas/place.py
from typing import Optional
from pydantic import BaseModel, Field

class PlaceCreate(BaseModel):
    name: str = Field(..., max_length=255)
    type: str = Field(..., max_length=50)
    is_frequent: bool = False
    atmosphere: Optional[str] = Field(None, max_length=20)
    pros: Optional[str] = Field(None, max_length=100)
    cons: Optional[str] = Field(None, max_length=100)
    image_url: Optional[str] = None

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

    class Config:
        from_attributes = True