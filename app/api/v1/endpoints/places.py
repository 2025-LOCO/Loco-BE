# app/api/v1/endpoints/places.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.place import PlaceCreate, PlaceOut
from app.crud import place as crud_place
from app.models import User
from app.utils.security import get_current_user

router = APIRouter(prefix="/places", tags=["places"])

@router.post("", response_model=PlaceOut)
def create_place(body: PlaceCreate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    return crud_place.create(db, user_id=current.id, obj_in=body)

@router.get("", response_model=List[PlaceOut])
def list_places(db: Session = Depends(get_db)):
    return crud_place.list_all(db)

@router.get("/{place_id}", response_model=PlaceOut, summary="장소 상세 조회")
def read_place_detail(place_id: int, db: Session = Depends(get_db)):
    obj = crud_place.get_by_id(db, place_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place not found")
    else:
        return obj