# app/api/v1/endpoints/routes.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.core.database import get_db
from app.schemas.route import RouteCreate, RouteOut, RouteExploreOut, HashTag, RoutePlace, Transportation
from app.crud import route as crud_route
from app.models import User, Route, RoutePlaceMap, Place, RegionCity
from app.utils.security import get_current_user

router = APIRouter(prefix="/routes", tags=["routes"])


# Route 모델 객체를 RouteOut 스키마로 변환하는 헬퍼 함수
def to_route_out(route: Route) -> RouteOut:
    # places, transportations 리스트 생성
    places_list = []
    transportations_list = []

    # route.places를 순서대로 정렬 (RoutePlaceMap.order 기준)
    sorted_places = sorted(route.places, key=lambda p: p.order)

    for rpm in sorted_places:
        if rpm.place:  # place 정보가 있는 경우
            places_list.append(RoutePlace(
                place_id=rpm.place.place_id,
                name=rpm.place.name,
                image_url=rpm.place.image_url,
                latitude=rpm.place.latitude,
                longitude=rpm.place.longitude,
            ))
        if rpm.is_transportation and rpm.transportation_name:
            transportations_list.append(Transportation(name=rpm.transportation_name))

    return RouteOut(
        route_id=route.route_id,
        name=route.name,
        is_recommend=route.is_recommend,
        image_url=route.image_url,
        count_real=route.count_real,
        count_normal=route.count_normal,
        count_bad=route.count_bad,
        user_id=route.created_by,
        # creator와 city 관계를 통해 city_name을 가져옴
        city_name=route.creator.city.kor_name if route.creator and route.creator.city else None,
        # liked는 count_real (진짜예요) 투표 수로 설정
        liked=route.count_real,
        tags=HashTag(
            period=route.tag_period,
            env=route.tag_env,
            with_whom=route.tag_with,
            move=route.tag_move,
            atmosphere=route.tag_atmosphere,
            place_count=route.tag_place_count,
        ),
        places=places_list,
        transportations=transportations_list
    )


@router.get("/explore", response_model=RouteExploreOut, summary="루트 탐색 페이지 데이터 조회")
def get_route_explore(db: Session = Depends(get_db)):
    # Eager loading을 사용하여 N+1 문제 방지
    ranked_routes_db = crud_route.get_ranked_routes(db, limit=25)
    new_routes_db = crud_route.get_new_routes(db, limit=25)

    ranked_routes = [to_route_out(r) for r in ranked_routes_db]
    new_routes = [to_route_out(r) for r in new_routes_db]

    return RouteExploreOut(
        ranked_routes=ranked_routes,
        new_routes=new_routes
    )


@router.post("", response_model=RouteOut)
def create_route(body: RouteCreate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    route = crud_route.create(db, user_id=current.id, obj_in=body)
    # 생성 후에도 joinedload를 사용하여 관련 데이터를 로드해야 함
    db.refresh(route, attribute_names=['creator', 'places'])
    return to_route_out(route)


@router.get("", response_model=List[RouteOut], summary="모든 경로 목록 조회")
def list_routes(db: Session = Depends(get_db)):
    routes_db = crud_route.list_all(db)
    return [to_route_out(r) for r in routes_db]


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
    routes_db = crud_route.search_by_tags(
        db,
        tag_period=tag_period,
        tag_env=tag_env,
        tag_with=tag_with,
        tag_move=tag_move,
        tag_atmosphere=tag_atmosphere,
        tag_place_count=tag_place_count,
    )
    return [to_route_out(r) for r in routes_db]


@router.get("/{route_id}", response_model=RouteOut, summary="경로 상세 조회")
def read_route_detail(route_id: int, db: Session = Depends(get_db)):
    obj = db.query(Route).options(
        joinedload(Route.creator).joinedload(User.city),
        joinedload(Route.places).joinedload(RoutePlaceMap.place)
    ).filter(Route.route_id == route_id).first()

    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found")
    return to_route_out(obj)