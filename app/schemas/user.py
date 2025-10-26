# app/schemas/user.py
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from app.models.user import UserGrade

class UserBase(BaseModel):
    email: EmailStr
    nickname: str = Field(..., max_length=10)
    intro: Optional[str] = Field(None, max_length=50)
    city_id: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserUpdate(BaseModel):
    nickname: Optional[str] = Field(None, max_length=10)
    intro: Optional[str] = Field(None, max_length=50)
    image_url: Optional[str] = Field(None, max_length=255)
    city_id: Optional[str] = None

class UserOut(BaseModel):
    id: int
    email: EmailStr
    nickname: str
    intro: Optional[str]
    image_url: Optional[str]
    city_id: Optional[str]
    created_at: datetime
    ranking: Optional[int]
    points: int
    grade: UserGrade
    my_places_count: int = 0
    my_routes_count: int = 0
    my_answers_count: int = 0
    my_places_liked_count: int = 0
    my_routes_liked_count: int = 0
    places_loco_count: List[int] = [0, 0, 0]
    routes_loco_count: List[int] = [0, 0, 0]

    class Config:
        from_attributes = True

class UserPublic(BaseModel):
    id: int
    nickname: Optional[str] = None
    city_name: Optional[str] = None
    intro: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: Optional[datetime] = None
    ranking: Optional[int]
    points: int
    grade: UserGrade
    ranking_percentile: Optional[float] = None
    liked: int

    class Config:
        from_attributes = True

class ProfileSearchResult(BaseModel):
    id: int
    name: str
    intro: Optional[str] = None
    image_url: Optional[str] = None
    liked: int
    rank: Optional[int] = None
    location: Optional[str] = None

class LocoExploreOut(BaseModel):
    best_users: List[UserPublic]
    new_local_users: List[UserPublic]