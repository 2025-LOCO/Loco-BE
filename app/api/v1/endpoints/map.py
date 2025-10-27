# app/api/v1/endpoints/map.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import place as crud_place
from app.crud.user import crud_user
from app.crud.favorite import list_my_favorite_places
from app.schemas.place import PlaceOut
from app.utils.security import get_current_user


router = APIRouter(prefix="/map", tags=["map"])

@router.get("/places", response_model=List[PlaceOut])
def read_places_for_map(db: Session = Depends(get_db)):
    places = crud_place.list_all(db)
    return places


@router.get(
    "/{user_id}/favorites",
    response_model=List[PlaceOut],
    summary="특정 유저가 찜한 장소 목록",
)
def get_user_favorite_places(user_id: int, db: Session = Depends(get_db)):
    """
    주어진 user_id를 가진 유저가 찜한 장소 목록을 반환합니다.
    """
    favorites = list_my_favorite_places(db, user_id=user_id)
    return [fav.place for fav in favorites]