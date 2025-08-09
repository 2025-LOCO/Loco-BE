from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.crud.trip import crud_trip
from app.crud.region import crud_region
from app.crud.user import crud_user
from app.models.trip import Trip
from app.models.user import User
from app.schemas.trip import TripCreate, TripUpdate


class TripService:
    @staticmethod
    def create_trip(db: Session, trip_data: TripCreate, user: User) -> Trip:
        """새 여행 계획 생성"""
        # 지역 존재 확인
        region = crud_region.get(db, id=trip_data.region_id)
        if not region:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Region not found"
            )

        # 하위 지역 확인 (있는 경우)
        if trip_data.sub_region_id:
            sub_region = crud_region.get(db, id=trip_data.sub_region_id)
            if not sub_region:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Sub region not found"
                )

        # 날짜 유효성 검사
        if trip_data.start_date and trip_data.end_date:
            if trip_data.start_date >= trip_data.end_date:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="End date must be after start date"
                )

        trip = crud_trip.create_with_user(db, obj_in=trip_data, user_id=user.id)
        return trip

    @staticmethod
    def update_trip(db: Session, trip_id: int, trip_data: TripUpdate, user: User) -> Trip:
        """여행 계획 수정"""
        trip = crud_trip.get(db, id=trip_id)
        if not trip:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Trip not found"
            )

        # 소유자 확인
        if trip.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

        # 날짜 유효성 검사
        start_date = trip_data.start_date if trip_data.start_date is not None else trip.start_date
        end_date = trip_data.end_date if trip_data.end_date is not None else trip.end_date

        if start_date and end_date and start_date >= end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="End date must be after start date"
            )

        trip = crud_trip.update(db, db_obj=trip, obj_in=trip_data)
        return trip

    @staticmethod
    def delete_trip(db: Session, trip_id: int, user: User) -> bool:
        """여행 계획 삭제"""
        trip = crud_trip.get(db, id=trip_id)
        if not trip:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Trip not found"
            )

        # 소유자 확인
        if trip.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

        crud_trip.remove(db, id=trip_id)
        return True

    @staticmethod
    def get_public_trips_by_region(db: Session, region_id: int, skip: int = 0, limit: int = 100) -> List[Trip]:
        """지역별 공개 여행 계획 조회"""
        return db.query(Trip).filter(
            Trip.region_id == region_id,
            Trip.is_public == True
        ).offset(skip).limit(limit).all()

    @staticmethod
    def get_recommended_trips_for_user(db: Session, user: User, limit: int = 10) -> List[Trip]:
        """사용자 맞춤 추천 여행 계획"""
        # 간단한 추천 로직: 사용자가 만든 여행과 같은 지역의 다른 공개 여행들
        user_regions = db.query(Trip.region_id).filter(Trip.user_id == user.id).distinct().all()
        region_ids = [region[0] for region in user_regions]

        if not region_ids:
            # 사용자 여행이 없으면 인기 여행 반환
            return crud_trip.get_public_trips(db, skip=0, limit=limit)

        recommended_trips = db.query(Trip).filter(
            Trip.region_id.in_(region_ids),
            Trip.user_id != user.id,
            Trip.is_public == True
        ).limit(limit).all()

        return recommended_trips


trip_service = TripService()