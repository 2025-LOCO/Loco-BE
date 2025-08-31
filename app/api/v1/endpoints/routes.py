# app/api/v1/endpoints/routes.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.route import RouteCreate, RouteOut
from app.crud import route as crud_route
from app.models import User
from app.utils.security import get_current_user

router = APIRouter(prefix="/routes", tags=["routes"])

@router.post("", response_model=RouteOut)
def create_route(body: RouteCreate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    return crud_route.create(db, user_id=current.id, obj_in=body)

@router.get("", response_model=List[RouteOut], summary="모든 경로 목록 조회")
def list_routes(db: Session = Depends(get_db)):
    return crud_route.list_all(db)

@router.get("/search", response_model=List[RouteOut], summary="태그로 경로 검색")
def search_routes(
    db: Session = Depends(get_db),
    tag_period: Optional[int] = Query(None, description="여행 기간 (일)"),
    tag_env: Optional[str] = Query(None, description="여행 환경 (e.g., sea, mountain)"),
    tag_with: Optional[str] = Query(None, description="동행 (e.g., alone, friend)"),
    tag_move: Optional[str] = Query(None, description="이동 수단 (e.g., car, public)"),
    tag_atmosphere: Optional[str] = Query(None, description="분위기 (e.g., 자유롭고 감성적인)"),
    tag_place_count: Optional[int] = Query(None, description="하루 방문 장소 수"),
):
    return crud_route.search_by_tags(
        db,
        tag_period=tag_period,
        tag_env=tag_env,
        tag_with=tag_with,
        tag_move=tag_move,
        tag_atmosphere=tag_atmosphere,
        tag_place_count=tag_place_count,
    )

@router.get("/{route_id}", response_model=RouteOut, summary="경로 상세 조회")
def read_route_detail(route_id: int, db: Session = Depends(get_db)):
    obj = crud_route.get_by_id(db, route_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found")
    return obj