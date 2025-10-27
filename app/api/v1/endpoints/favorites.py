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
from app.utils.security import get_current_user, get_optional_current_user
from app.api.v1.endpoints.routes import to_loco_route
from app.crud import place as crud_place
from app.schemas.place import PlaceOut
from app.schemas.route import RouteOut


router = APIRouter(prefix="/favorites", tags=["favorites"])

# Add to favorites
@router.post("/places", response_model=FavoritePlaceOut, status_code=status.HTTP_201_CREATED)
def add_fav_place(body: FavoritePlaceCreate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    return crud_fav.add_favorite_place(db, current.id, body.place_id)

@router.post("/routes", response_model=FavoriteRouteOut, status_code=status.HTTP_201_CREATED)
def add_fav_route(body: FavoriteRouteCreate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    return crud_fav.add_favorite_route(db, current.id, body.route_id)

# NEW: list my favorites
@router.get("/places/{user_id}", response_model=List[FavoritePlaceOut])
def list_my_fav_places(user_id: int, db: Session = Depends(get_db)):
    return crud_fav.list_my_favorite_places(db, user_id)

@router.get("/routes/{user_id}", response_model=List[FavoriteRouteOut])
def list_my_fav_routes(user_id: int, db: Session = Depends(get_db)):
    favorite_routes = crud_fav.list_my_favorite_routes(db, user_id)
    
    response = []
    for fav_route in favorite_routes:
        processed_route = to_loco_route(fav_route.route) if fav_route.route else None
        response.append(FavoriteRouteOut(
            id=fav_route.id,
            user_id=fav_route.user_id,
            route_id=fav_route.route_id,
            created_at=fav_route.created_at,
            route=processed_route
        ))
    return response

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


@router.get("/places/ids", summary="찜한 장소 ID 목록 조회")
def get_my_favorite_place_ids(
    current_user: User = Depends(get_optional_current_user),
    db: Session = Depends(get_db),
):
    if not current_user:
        return []
    favorites = crud_fav.list_my_favorite_places(db, current_user.id)
    return [fav.place_id for fav in favorites]


@router.get(
    "/places",
    response_model=List[PlaceOut],
    summary="현재 유저가 찜한 장소 목록",
)
def get_my_favorite_places(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    favorites = crud_fav.list_my_favorite_places(db, current_user.id)
    return [fav.place for fav in favorites]