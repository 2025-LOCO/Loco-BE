# app/api/v1/endpoints/favorites.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.favorite import FavoritePlaceCreate, FavoriteRouteCreate
from app.crud import favorite as crud_fav
from app.models import User
from app.utils.security import get_current_user

router = APIRouter(prefix="/api/v1/favorites", tags=["favorites"])

@router.post("/places")
def add_fav_place(body: FavoritePlaceCreate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    return crud_fav.add_favorite_place(db, current.id, body.place_id)

@router.post("/routes")
def add_fav_route(body: FavoriteRouteCreate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    return crud_fav.add_favorite_route(db, current.id, body.route_id)