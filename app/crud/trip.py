from typing import List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.trip import Trip
from app.schemas.trip import TripCreate, TripUpdate

class CRUDTrip(CRUDBase[Trip, TripCreate, TripUpdate]):
    def get_by_user(self, db: Session, *, user_id: int) -> List[Trip]:
        return db.query(Trip).filter(Trip.user_id == user_id).all()

    def get_public_trips(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Trip]:
        return db.query(Trip).filter(Trip.is_public == True).offset(skip).limit(limit).all()

    def create_with_user(self, db: Session, *, obj_in: TripCreate, user_id: int) -> Trip:
        db_obj = Trip(**obj_in.dict(), user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

crud_trip = CRUDTrip(Trip)