# app/api/v1/endpoints/favorites.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.favorite import (
    FavoritePlaceCreate, FavoriteRouteCreate,
    FavoritePlaceOut, FavoriteRouteOut,
)
from app.crud import favorite as crud_fav
from app.models import User
from app.utils.security import get_current_user

router = APIRouter(prefix="/favorites", tags=["favorites"])

# Add to favorites
@router.post("/places", response_model=FavoritePlaceOut, status_code=status.HTTP_201_CREATED)
def add_fav_place(body: FavoritePlaceCreate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    return crud_fav.add_favorite_place(db, current.id, body.place_id)

@router.post("/routes", response_model=FavoriteRouteOut, status_code=status.HTTP_201_CREATED)
def add_fav_route(body: FavoriteRouteCreate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    return crud_fav.add_favorite_route(db, current.id, body.route_id)

# NEW: list my favorites
@router.get("/places/me", response_model=List[FavoritePlaceOut])
def list_my_fav_places(db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    return crud_fav.list_my_favorite_places(db, current.id)

@router.get("/routes/me", response_model=List[FavoriteRouteOut])
def list_my_fav_routes(db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    return crud_fav.list_my_favorite_routes(db, current.id)

# NEW: remove from favorites
@router.delete("/places/{place_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_fav_place(place_id: int, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    ok = crud_fav.remove_favorite_place(db, current.id, place_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Favorite place not found")
    return None

@router.delete("/routes/{route_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_fav_route(route_id: int, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    ok = crud_fav.remove_favorite_route(db, current.id, route_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Favorite route not found")
    return None