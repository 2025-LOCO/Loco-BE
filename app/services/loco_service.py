from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from fastapi import HTTPException, status
from app.crud.loco import crud_loco
from app.crud.user import crud_user
from app.crud.region import crud_region
from app.models.loco import Loco
from app.models.user import User
from app.schemas.loco import LocoCreate, LocoUpdate


class LocoService:
    @staticmethod
    def create_loco_profile(db: Session, loco_data: LocoCreate, user: User) -> Loco:
        """로코 프로필 생성"""
        # 이미 로코 프로필이 있는지 확인
        existing_loco = crud_loco.get_by_user(db, user_id=user.id)
        if existing_loco:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Loco profile already exists"
            )

        # 지역 존재 확인
        region = crud_region.get(db, id=loco_data.region_id)
        if not region:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Region not found"
            )

        # 사용자를 로코로 설정
        user.is_loco = True
        db.add(user)

        loco = crud_loco.create_with_user(db, obj_in=loco_data, user_id=user.id)
        db.commit()
        return loco

    @staticmethod
    def update_loco_profile(db: Session, loco_data: LocoUpdate, user: User) -> Loco:
        """로코 프로필 수정"""
        loco = crud_loco.get_by_user(db, user_id=user.id)
        if not loco:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Loco profile not found"
            )

        loco = crud_loco.update(db, db_obj=loco, obj_in=loco_data)
        return loco

    @staticmethod
    def get_locos_by_region(
            db: Session,
            region_id: int,
            min_rating: float = 0.0,
            max_hourly_rate: Optional[int] = None,
            is_verified: Optional[bool] = None,
            skip: int = 0,
            limit: int = 100
    ) -> List[Loco]:
        """지역별 로코 검색 (필터링 옵션 포함)"""
        query = db.query(Loco).filter(
            Loco.region_id == region_id,
            Loco.is_available == True,
            Loco.rating >= min_rating
        )

        if max_hourly_rate is not None:
            query = query.filter(Loco.hourly_rate <= max_hourly_rate)

        if is_verified is not None:
            query = query.filter(Loco.is_verified == is_verified)

        return query.order_by(Loco.rating.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_top_rated_locos(db: Session, limit: int = 10) -> List[Loco]:
        """최고 평점 로코들"""
        return db.query(Loco).filter(
            Loco.is_available == True,
            Loco.review_count > 0
        ).order_by(
            Loco.rating.desc(),
            Loco.review_count.desc()
        ).limit(limit).all()

    @staticmethod
    def search_locos_by_specialty(
            db: Session,
            specialty: str,
            region_id: Optional[int] = None,
            skip: int = 0,
            limit: int = 100
    ) -> List[Loco]:
        """전문 분야로 로코 검색"""
        query = db.query(Loco).filter(
            Loco.is_available == True,
            Loco.specialties.contains(specialty)
        )

        if region_id:
            query = query.filter(Loco.region_id == region_id)

        return query.order_by(Loco.rating.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def update_loco_rating(db: Session, loco_id: int, new_rating: float) -> Loco:
        """로코 평점 업데이트 (리뷰 시스템과 연동용)"""
        loco = crud_loco.get(db, id=loco_id)
        if not loco:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Loco not found"
            )

        # 새로운 평점 계산 (기존 평점과 새 평점의 가중평균)
        total_rating_points = loco.rating * loco.review_count + new_rating
        loco.review_count += 1
        loco.rating = round(total_rating_points / loco.review_count, 2)

        db.add(loco)
        db.commit()
        db.refresh(loco)
        return loco

    @staticmethod
    def get_loco_statistics(db: Session, region_id: Optional[int] = None) -> Dict[str, Any]:
        """로코 통계 정보"""
        query = db.query(Loco).filter(Loco.is_available == True)

        if region_id:
            query = query.filter(Loco.region_id == region_id)

        total_locos = query.count()
        verified_locos = query.filter(Loco.is_verified == True).count()
        avg_rating = query.with_entities(func.avg(Loco.rating)).scalar() or 0
        avg_hourly_rate = query.filter(Loco.hourly_rate.isnot(None)).with_entities(
            func.avg(Loco.hourly_rate)).scalar() or 0

        return {
            "total_locos": total_locos,
            "verified_locos": verified_locos,
            "verification_rate": round(verified_locos / total_locos * 100, 2) if total_locos > 0 else 0,
            "average_rating": round(avg_rating, 2),
            "average_hourly_rate": round(avg_hourly_rate, 2)
        }

    @staticmethod
    def toggle_loco_availability(db: Session, user: User) -> Loco:
        """로코 활성/비활성 상태 토글"""
        loco = crud_loco.get_by_user(db, user_id=user.id)
        if not loco:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Loco profile not found"
            )

        loco.is_available = not loco.is_available
        db.add(loco)
        db.commit()
        db.refresh(loco)
        return loco


loco_service = LocoService()