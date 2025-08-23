# app/schemas/favorite.py
from pydantic import BaseModel

class FavoritePlaceCreate(BaseModel):
    place_id: int

class FavoriteRouteCreate(BaseModel):
    route_id: int