# app/api/v1/endpoints/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserOut, UserUpdate, UserPublic, LocoExploreOut
from app.models import User
from app.crud.user import crud_user
from app.utils.security import get_current_user  # 토큰에서 사용자 로드(예시 아래)

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserOut)
def me(current: User = Depends(get_current_user)):
    return current


@router.get("/loco-explore", response_model=LocoExploreOut, summary="로코탐색 페이지 데이터 조회")
def get_loco_explore_users(db: Session = Depends(get_db)):
    best_users_db = crud_user.get_best_users(db, limit=25)
    new_local_users_db = crud_user.get_new_local_users(db, limit=25)

    # 랭킹 백분율 계산을 위해 전체 랭킹 유저 수를 가져옵니다.
    total_ranked_users = crud_user.get_total_ranked_user_count(db)

    # 응답 데이터를 담을 리스트를 준비합니다.
    best_users_response = []
    if total_ranked_users > 0:
        for user in best_users_db:
            user_data = UserPublic.model_validate(user)
            if user.ranking:
                # (개인 순위 / 전체 인원) * 100 으로 백분율 계산
                user_data.ranking_percentile = (user.ranking / total_ranked_users) * 100
            best_users_response.append(user_data)

    new_local_users_response = []
    if total_ranked_users > 0:
        for user in new_local_users_db:
            user_data = UserPublic.model_validate(user)
            if user.ranking:
                # 신규 로코지기 목록에도 동일하게 백분율 계산
                user_data.ranking_percentile = (user.ranking / total_ranked_users) * 100
            new_local_users_response.append(user_data)

    return LocoExploreOut(
        best_users=best_users_response,
        new_local_users=new_local_users_response
    )

@router.put("/me", response_model=UserOut)
def update_me(payload: UserUpdate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    current.nickname = payload.nickname or current.nickname
    current.intro = payload.intro if payload.intro is not None else current.intro
    current.city_id = payload.city_id if payload.city_id is not None else current.city_id
    db.commit()
    db.refresh(current)
    return current

@router.get("/{user_id}", response_model=UserPublic, summary="다른 사용자 프로필 상세 조회")
def read_user_public_profile(user_id: int, db: Session = Depends(get_db)):
    obj = crud_user.get_by_id(db, user_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # 필요한 공개 필드만 매핑; 모델 필드명에 맞게 조정
    return UserPublic.model_validate(obj)

@router.delete("/me", status_code=204, summary="회원 탈퇴")
def delete_me(db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    # 추가 보안: DB에서 최신 상태를 재로딩 (선택)
    user = db.get(User, current.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 발급된 토큰 즉시 무효화를 위해 버전 증가(선택적이지만 권장)
    user.token_version += 1
    db.delete(user)
    db.commit()
    # 204 No Content
    return

