# app/crud/route.py
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import case, func, Float
from app.models import Route
from app.schemas.route import RouteCreate
from app.services.vector_service import text_to_vector

def create(db: Session, user_id: int, obj_in: RouteCreate) -> Route:
    tags_text = (
        f"{obj_in.tag_env or ''} "
        f"{obj_in.tag_with or ''} "
        f"{obj_in.tag_atmosphere or ''}"
    )
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
        embedding=embedding_vector
    )
    db.add(route)
    db.commit()
    db.refresh(route)
    return route

def get_by_id(db: Session, route_id: int) -> Optional[Route]:
    return db.query(Route).filter(Route.route_id == route_id).first()

def list_all(db: Session, limit: int = 50, offset: int = 0) -> List[Route]:
    return (
        db.query(Route)
        .order_by(Route.route_id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

def search_by_tags(
    db: Session,
    limit: int = 50,
    offset: int = 0,
    tag_period: Optional[int] = None,
    tag_env: Optional[str] = None,
    tag_with: Optional[str] = None,
    tag_move: Optional[str] = None,
    tag_atmosphere: Optional[str] = None,
    tag_place_count: Optional[int] = None,
) -> List[Route]:
    query = db.query(Route)

    if tag_period is not None:
        query = query.filter(Route.tag_period == tag_period)
    if tag_env:
        query = query.filter(Route.tag_env == tag_env)
    if tag_with:
        query = query.filter(Route.tag_with == tag_with)
    if tag_move:
        query = query.filter(Route.tag_move == tag_move)
    if tag_atmosphere:
        query = query.filter(Route.tag_atmosphere == tag_atmosphere)
    if tag_place_count is not None:
        query = query.filter(Route.tag_place_count == tag_place_count)

    return (
        query.order_by(Route.route_id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


def get_ranked_routes(db: Session, limit: int = 25) -> List[Route]:
    n = (Route.count_real + Route.count_bad).cast(Float)
    z = 1.96  # 95% 신뢰수준

    # 윌슨 스코어 계산식을 CASE 안으로 이동하여 0으로 나누기 오류를 원천 방지
    ranking_score = case(
        (n > 0, (
            (Route.count_real.cast(Float) / n + (z*z) / (2*n) - z * func.sqrt(( (Route.count_real.cast(Float) / n) * (1 - (Route.count_real.cast(Float) / n)) + (z*z) / (4*n) ) / n)) / (1 + (z*z)/n)
        )),
        else_=0.0
    ).label("ranking_score")

    return db.query(Route).order_by(ranking_score.desc()).limit(limit).all()

def get_new_routes(db: Session, limit: int = 25) -> List[Route]:
    return db.query(Route).order_by(Route.created_at.desc()).limit(limit).all()