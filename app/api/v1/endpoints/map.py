# app/api/v1/endpoints/map.py

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.place import PlaceOut
from app.crud import place as crud_place

router = APIRouter(prefix="/map", tags=["map"])

@router.get("/places", response_model=List[PlaceOut])
def read_places_for_map(db: Session = Depends(get_db)):
    places = crud_place.list_all(db)
    return places