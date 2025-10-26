# app/schemas/favorite.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.schemas.place import PlaceOut
from app.schemas.route import LocoRoute

class FavoritePlaceCreate(BaseModel):
    place_id: int

class FavoriteRouteCreate(BaseModel):
    route_id: int

# NEW: Out schemas including nested objects
class FavoritePlaceOut(BaseModel):
    id: int
    user_id: int
    place_id: int
    created_at: datetime
    place: Optional[PlaceOut]

    class Config:
        from_attributes = True

class FavoriteRouteOut(BaseModel):
    id: int
    user_id: int
    route_id: int
    created_at: datetime
    route: Optional[LocoRoute]

    class Config:
        from_attributes = True