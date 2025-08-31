# app/crud/route.py
from typing import Optional
from sqlalchemy.orm import Session
from app.models import Route
from app.schemas.route import RouteCreate
from app.services.vector_service import text_to_vector

def create(db: Session, user_id: int, obj_in: RouteCreate) -> Route:
    # 태그들을 모아 하나의 문장으로 만듦
    tags_text = (
        f"{obj_in.tag_env or ''} "
        f"{obj_in.tag_with or ''} "
        f"{obj_in.tag_atmosphere or ''}"
    )

    # 문장이 있을 경우에만 벡터로 변환
    embedding_vector = text_to_vector(tags_text) if tags_text.strip() else None

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
        embedding=embedding_vector  # 변환된 벡터를 함께 저장
    )
    db.add(route)
    db.commit()
    db.refresh(route)
    return route

def get_by_id(db: Session, route_id: int) -> Optional[Route]:
    return db.query(Route).filter(Route.route_id == route_id).first()

def list_all(db: Session, limit: int = 50, offset: int = 0) -> list[Route]:
    return (
        db.query(Route)
        .order_by(Route.route_id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )