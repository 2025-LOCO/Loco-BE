# app/crud/favorite.py
from typing import List
from sqlalchemy.orm import Session, joinedload
from app.models import FavoritePlace, FavoriteRoute, Place, Route

def add_favorite_place(db: Session, user_id: int, place_id: int) -> FavoritePlace:
    obj = db.query(FavoritePlace).filter_by(user_id=user_id, place_id=place_id).first()
    if obj:
        return obj
    obj = FavoritePlace(user_id=user_id, place_id=place_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def add_favorite_route(db: Session, user_id: int, route_id: int) -> FavoriteRoute:
    obj = db.query(FavoriteRoute).filter_by(user_id=user_id, route_id=route_id).first()
    if obj:
        return obj
    obj = FavoriteRoute(user_id=user_id, route_id=route_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

# NEW: list current user's favorites
def list_my_favorite_places(db: Session, user_id: int) -> List[FavoritePlace]:
    return (
        db.query(FavoritePlace)
        .options(joinedload(FavoritePlace.place))
        .filter(FavoritePlace.user_id == user_id)
        .order_by(FavoritePlace.created_at.desc())
        .all()
    )

def list_my_favorite_routes(db: Session, user_id: int) -> List[FavoriteRoute]:
    return (
        db.query(FavoriteRoute)
        .options(joinedload(FavoriteRoute.route))
        .filter(FavoriteRoute.user_id == user_id)
        .order_by(FavoriteRoute.created_at.desc())
        .all()
    )

# NEW: remove from favorites
def remove_favorite_place(db: Session, user_id: int, place_id: int) -> bool:
    obj = db.query(FavoritePlace).filter_by(user_id=user_id, place_id=place_id).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True

def remove_favorite_route(db: Session, user_id: int, route_id: int) -> bool:
    obj = db.query(FavoriteRoute).filter_by(user_id=user_id, route_id=route_id).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True