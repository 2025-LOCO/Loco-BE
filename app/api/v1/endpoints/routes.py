# app/api/v1/endpoints/routes.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.core.database import get_db
from app.schemas.route import RouteCreate, RouteOut, RouteExploreOut, HashTag, RoutePlace, Transportation, LocoRoute
from app.crud import route as crud_route
from app.models import User, Route, RoutePlaceMap, Place, RegionCity
from app.utils.security import get_current_user

router = APIRouter(prefix="/routes", tags=["routes"])


def to_loco_route(route: "Route") -> LocoRoute:
    # places 및 transportations 정보 가공
    places_schema = []
    transportations_schema = []
    
    # day와 order로 정렬
    sorted_places = sorted(route.places, key=lambda p: (p.day, p.order))
    
    for p_map in sorted_places:
        # RoutePlace 스키마 생성
        places_schema.append(RoutePlace(
            id=p_map.place.place_id,
            name=p_map.place.name,
            category=p_map.place.type,
            day=p_map.day,
            order=p_map.order
        ))
        
        # Transportation 스키마 생성 (중복 제거 로직 포함)
        if p_map.transportation:
            # 같은 day, order를 가진 transportation이 이미 있는지 확인
            exists = any(t.day == p_map.day and t.order == p_map.order for t in transportations_schema)
            if not exists:
                transportations_schema.append(Transportation(
                    id=len(transportations_schema) + 1, # 임시 ID
                    name=p_map.transportation,
                    day=p_map.day,
                    order=p_map.order
                ))

    # 태그 정보 가공
    tags_schema = HashTag(
        period=str(route.tag_period or ''),
        env=str(route.tag_env or ''),
        with_who=str(route.tag_with or ''),
        move=str(route.tag_move or ''),
        atmosphere=str(route.tag_atmosphere or ''),
        place_count=str(route.tag_place_count or '')
    )

    return LocoRoute(
        user_id=route.created_by,
        id=route.route_id,
        name=route.name,
        image_url=route.image_url,
        location=route.location,
        intro=route.intro,
        liked=route.count_real,  # TODO: 'liked' 필드를 즐겨찾기 수로 변경해야 함
        tags=tags_schema,
        places=places_schema,
        transportations=transportations_schema,
        count_real=route.count_real,
        count_soso=route.count_soso,
        count_bad=route.count_bad,
        created_at=route.created_at,
    )


@router.get("/explore", response_model=RouteExploreOut, summary="루트 탐색 페이지 데이터 조회")
def get_route_explore(db: Session = Depends(get_db)):
    ranked_routes_db = crud_route.get_ranked_routes(db, limit=25)
    new_routes_db = crud_route.get_new_routes(db, limit=25)
    
    ranked_routes = [to_loco_route(r) for r in ranked_routes_db]
    new_routes = [to_loco_route(r) for r in new_routes_db]
    
    return RouteExploreOut(
        rankedRoutes=ranked_routes,
        newRoutes=new_routes
    )


@router.post("", status_code=status.HTTP_201_CREATED)
def create_route(body: RouteCreate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    try:
        crud_route.create(db, user_id=current.id, obj_in=body)
        return {"message": "Route created successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )


@router.get("", response_model=List[LocoRoute], summary="모든 경로 목록 조회")
def list_routes(db: Session = Depends(get_db)):
    routes_db = crud_route.list_all(db)
    return [to_loco_route(r) for r in routes_db]


@router.get("/search", response_model=List[LocoRoute], summary="태그로 경로 검색")
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
    return [to_loco_route(r) for r in routes_db]


@router.get("/{route_id}", response_model=LocoRoute, summary="경로 상세 조회")
def read_route_detail(route_id: int, db: Session = Depends(get_db)):
    obj = db.query(Route).options(
        joinedload(Route.creator).joinedload(User.city),
        joinedload(Route.places).joinedload(RoutePlaceMap.place)
    ).filter(Route.route_id == route_id).first()

    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found")
    return to_loco_route(obj)