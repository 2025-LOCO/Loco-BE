# app/schemas/user.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

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
    city_id: Optional[str] = None

class UserOut(BaseModel):
    id: int
    email: EmailStr
    nickname: str
    intro: Optional[str]
    city_id: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True