# app/api/v1/endpoints/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.core.database import get_db
from app.schemas.user import UserOut, UserUpdate, UserPublic, LocoExploreOut, ProfileSearchResult
from app.models import User, RegionCity
from app.crud.user import crud_user
from app.utils.security import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


# --- 순서 보장을 위해 고정 경로를 먼저 배치 ---

@router.get("/me", response_model=UserOut)
def me(current: User = Depends(get_current_user)):
    return current


def to_profile_search_result(user: User) -> ProfileSearchResult:
    # '담아요' 수 계산 로직
    total_likes = 0
    if user.created_places:
        total_likes += sum(p.count_real for p in user.created_places)
    if user.created_routes:
        total_likes += sum(r.count_real for r in user.created_routes)
    
    return ProfileSearchResult(
        id=user.id,
        name=user.nickname,
        intro=user.intro,
        image_url=user.image_url,
        liked=total_likes,
        rank=user.ranking,
        location=user.city.kor_name if user.city else None
    )


@router.get("/explore", response_model=List[ProfileSearchResult], summary="프로필 탐색 페이지 데이터 조회")
def get_user_explore(db: Session = Depends(get_db)):
    best_users_db = crud_user.get_best_users(db, limit=50) # 예시로 50명 조회
    
    return [to_profile_search_result(u) for u in best_users_db]


@router.get("/loco-explore", response_model=LocoExploreOut, summary="로코탐색 페이지 데이터 조회")
def get_loco_explore_users(db: Session = Depends(get_db)):
    # crud 함수에서 이미 Eager Loading을 통해 데이터를 가져옵니다.
    best_users_db = crud_user.get_best_users(db, limit=25)
    new_local_users_db = crud_user.get_new_local_users(db, limit=25)

    total_ranked_users = crud_user.get_total_ranked_user_count(db)

    def to_user_public(user: User, total_ranked: int) -> UserPublic:
        # '담아요' 수 계산 로직
        total_likes = 0
        if user.created_places:
            total_likes += sum(p.count_real for p in user.created_places)
        if user.created_routes:
            total_likes += sum(r.count_real for r in user.created_routes)

        user_data = UserPublic(
            id=user.id,
            nickname=user.nickname,
            intro=user.intro,
            created_at=user.created_at,
            ranking=user.ranking,
            points=user.points,
            grade=user.grade,
            liked=total_likes,  # 계산된 합계 값을 사용
            city_name=user.city.kor_name if user.city else None,
            ranking_percentile=(user.ranking / total_ranked) * 100 if user.ranking and total_ranked > 0 else None
        )
        return user_data

    best_users_response = [to_user_public(u, total_ranked_users) for u in best_users_db]
    new_local_users_response = [to_user_public(u, total_ranked_users) for u in new_local_users_db]

    return LocoExploreOut(
        best_users=best_users_response,
        new_local_users=new_local_users_response
    )


@router.put("/me", response_model=UserOut)
def update_me(payload: UserUpdate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    current.nickname = payload.nickname or current.nickname
    current.intro = payload.intro if payload.intro is not None else current.intro
    current.image_url = payload.image_url if payload.image_url is not None else current.image_url
    current.city_id = payload.city_id if payload.city_id is not None else current.city_id
    db.commit()
    db.refresh(current)
    return current


# --- 변수 경로를 마지막에 배치 ---

@router.get("/{user_id}", response_model=UserPublic, summary="다른 사용자 프로필 상세 조회")
def read_user_public_profile(user_id: int, db: Session = Depends(get_db)):
    obj = crud_user.get_by_id(db, user_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # '담아요' 수 계산 로직
    total_likes = 0
    if obj.created_places:
        total_likes += sum(p.count_real for p in obj.created_places)
    if obj.created_routes:
        total_likes += sum(r.count_real for r in obj.created_routes)

    user_data = UserPublic(
        id=obj.id,
        nickname=obj.nickname,
        intro=obj.intro,
        created_at=obj.created_at,
        ranking=obj.ranking,
        points=obj.points,
        grade=obj.grade,
        liked=total_likes,  # 계산된 합계 값을 사용
        city_name=obj.city.kor_name if obj.city else None,
    )
    return user_data


@router.delete("/me", status_code=204, summary="회원 탈퇴")
def delete_me(db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    user = db.get(User, current.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.token_version += 1
    db.delete(user)
    db.commit()
    return