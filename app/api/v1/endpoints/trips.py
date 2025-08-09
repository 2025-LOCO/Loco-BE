from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_active_user
from app.crud.trip import crud_trip
from app.models.user import User
from app.schemas.trip import Trip, TripCreate, TripUpdate

router = APIRouter()

@router.get("/", response_model=List[Trip])
def read_trips(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    trips = crud_trip.get_public_trips(db, skip=skip, limit=limit)
    return trips

@router.post("/", response_model=Trip)
def create_trip(
    *,
    db: Session = Depends(get_db),
    trip_in: TripCreate,
    current_user: User = Depends(get_current_active_user),
):
    trip = crud_trip.create_with_user(db, obj_in=trip_in, user_id=current_user.id)
    return trip

@router.get("/my", response_model=List[Trip])
def read_my_trips(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    trips = crud_trip.get_by_user(db, user_id=current_user.id)
    return trips