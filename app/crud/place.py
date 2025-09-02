# app/crud/place.py
from sqlalchemy.orm import Session
from sqlalchemy import case
from typing import List, Optional
from app.models import Place
from app.schemas.place import PlaceCreate

def create(db: Session, user_id: int, obj_in: PlaceCreate) -> Place:
    place = Place(
        name=obj_in.name,
        type=obj_in.type,
        is_frequent=obj_in.is_frequent,
        atmosphere=obj_in.atmosphere,
        pros=obj_in.pros,
        cons=obj_in.cons,
        image_url=obj_in.image_url,
        latitude=obj_in.latitude,
        longitude=obj_in.longitude,
        kakao_place_id=obj_in.kakao_place_id,
        created_by=user_id,
    )
    db.add(place)
    db.commit()
    db.refresh(place)
    return place

def list_all(db: Session, limit: int = 50, offset: int = 0) -> List[Place]:
    return db.query(Place).order_by(Place.place_id.desc()).offset(offset).limit(limit).all()

def get_by_id(db: Session, place_id: int) -> Optional[Place]:
    return db.query(Place).filter(Place.place_id == place_id).first()

def get_ranked_places(db: Session, limit: int = 5) -> List[Place]:
    ranking_score = case(
        ( (Place.count_real + Place.count_bad) > 0, Place.count_real / (Place.count_real + Place.count_bad) ),
        else_ = 0.0
    ).label("ranking_score")

    # 위에서 계산한 ranking_score를 기준으로 내림차순 정렬합니다.
    return db.query(Place).order_by(ranking_score.desc()).limit(limit).all()

def get_new_places(db: Session, limit: int = 5) -> List[Place]:
    return db.query(Place).order_by(Place.created_at.desc()).limit(limit).all()