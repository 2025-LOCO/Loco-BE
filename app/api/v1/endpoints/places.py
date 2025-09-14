# app/api/v1/endpoints/places.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.place import PlaceCreate, PlaceOut, PlaceExploreOut
from app.crud import place as crud_place
from app.models import User, Place # Place 모델 추가
from app.utils.security import get_current_user

router = APIRouter(prefix="/places", tags=["places"])

# Place 모델 객체를 PlaceOut 스키마로 변환하는 헬퍼 함수
def to_place_out(place: Place) -> PlaceOut:
    return PlaceOut(
        place_id=place.place_id,
        name=place.name,
        type=place.type,
        is_frequent=place.is_frequent,
        atmosphere=place.atmosphere,
        pros=place.pros,
        cons=place.cons,
        image_url=place.image_url,
        count_real=place.count_real,
        count_normal=place.count_normal,
        count_bad=place.count_bad,
        latitude=place.latitude,
        longitude=place.longitude,
        kakao_place_id=place.kakao_place_id,
        intro=place.intro,
        phone=place.phone,
        address_name=place.address_name,
        link=place.link,
        liked=place.count_real,  # '진짜예요' 투표 수를 liked로 설정
        user_id=place.created_by,
        city_name=place.creator.city.kor_name if place.creator and place.creator.city else None,
    )

@router.get("/explore", response_model=PlaceExploreOut, summary="장소 탐색 페이지 데이터 조회")
def get_place_explore(db: Session = Depends(get_db)):
    ranked_places_db = crud_place.get_ranked_places(db, limit=25)
    new_places_db = crud_place.get_new_places(db, limit=25)

    ranked_places = [to_place_out(p) for p in ranked_places_db]
    new_places = [to_place_out(p) for p in new_places_db]

    return PlaceExploreOut(
        ranked_places=ranked_places,
        new_places=new_places
    )

@router.post("", response_model=PlaceOut)
def create_place(body: PlaceCreate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    place = crud_place.create(db, user_id=current.id, obj_in=body)
    db.refresh(place, attribute_names=['creator']) # creator 관계를 리프레시
    return to_place_out(place)

@router.get("", response_model=List[PlaceOut])
def list_places(db: Session = Depends(get_db)):
    places_db = crud_place.list_all(db)
    return [to_place_out(p) for p in places_db]

@router.get("/{place_id}", response_model=PlaceOut, summary="장소 상세 조회")
def read_place_detail(place_id: int, db: Session = Depends(get_db)):
    obj = crud_place.get_by_id(db, place_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place not found")
    else:
        return to_place_out(obj)