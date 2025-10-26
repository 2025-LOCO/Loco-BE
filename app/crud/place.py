# app/crud/place.py
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import case, func, Float
from typing import List, Optional
from app.models import Place, User # User 모델 추가
from app.schemas.place import PlaceCreate

# 공통적으로 사용할 Eager Loading 옵션
eager_loading_options = [
    joinedload(Place.creator).joinedload(User.city)
]

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
        intro=obj_in.intro,
        phone=obj_in.phone,
        address_name=obj_in.address_name,
        link=obj_in.link,
    )
    db.add(place)
    db.commit()
    db.refresh(place)
    return place

def list_all(db: Session, limit: int = 50, offset: int = 0) -> List[Place]:
    return db.query(Place).options(*eager_loading_options).order_by(Place.place_id.desc()).offset(offset).limit(limit).all()

def get_by_id(db: Session, place_id: int) -> Optional[Place]:
    return db.query(Place).options(*eager_loading_options).filter(Place.place_id == place_id).first()


def get_ranked_places(db: Session, limit: int = 25) -> List[Place]:
    n = (Place.count_real + Place.count_bad).cast(Float)
    z = 1.96  # 95% 신뢰수준

    ranking_score = case(
        (n > 0, (
            (Place.count_real.cast(Float) / n + (z*z) / (2*n) - z * func.sqrt(( (Place.count_real.cast(Float) / n) * (1 - (Place.count_real.cast(Float) / n)) + (z*z) / (4*n) ) / n)) / (1 + (z*z)/n)
        )),
        else_=0.0
    ).label("ranking_score")

    return db.query(Place).options(*eager_loading_options).order_by(ranking_score.desc()).limit(limit).all()

def get_new_places(db: Session, limit: int = 25) -> List[Place]:
    return db.query(Place).options(*eager_loading_options).order_by(Place.created_at.desc()).limit(limit).all()

def count_by_user(db: Session, user_id: int) -> int:
    return db.query(Place).filter(Place.created_by == user_id).count()

def sum_likes_by_user(db: Session, user_id: int) -> int:
    total_likes = db.query(func.sum(Place.count_real)).filter(Place.created_by == user_id).scalar()
    return total_likes if total_likes is not None else 0

def sum_loco_count_by_user(db: Session, user_id: int) -> List[int]:
    result = db.query(
        func.sum(Place.count_real),
        func.sum(Place.count_normal),
        func.sum(Place.count_bad)
    ).filter(Place.created_by == user_id).first()
    return [result[0] or 0, result[1] or 0, result[2] or 0]