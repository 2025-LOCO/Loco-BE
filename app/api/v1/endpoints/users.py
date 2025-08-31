# app/api/v1/endpoints/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserOut, UserUpdate, UserPublic
from app.models import User
from app.crud.user import crud_user
from app.utils.security import get_current_user  # 토큰에서 사용자 로드(예시 아래)

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserOut)
def me(current: User = Depends(get_current_user)):
    return current

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