# app/crud/route.py
from sqlalchemy.orm import Session
from typing import List
from app.models import Route
from app.schemas.route import RouteCreate

def create(db: Session, user_id: int, obj_in: RouteCreate) -> Route:
    route = Route(
        name=obj_in.name,
        is_recommend=obj_in.is_recommend,
        image_url=obj_in.image_url,
        tag_period=obj_in.tag_period,
        tag_env=obj_in.tag_env,
        tag_with=obj_in.tag_with,
        tag_move=obj_in.tag_move,
        tag_atmosphere=obj_in.tag_atmosphere,
        tag_place_count=obj_in.tag_place_count,
        created_by=user_id,
    )
    db.add(route)
    db.commit()
    db.refresh(route)
    return route

def list_all(db: Session, limit: int = 50, offset: int = 0) -> List[Route]:
    return db.query(Route).order_by(Route.route_id.desc()).offset(offset).limit(limit).all()