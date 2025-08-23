# app/crud/favorite.py
from sqlalchemy.orm import Session
from app.models import FavoritePlace, FavoriteRoute

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