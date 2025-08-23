# app/api/v1/endpoints/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserOut, UserUpdate
from app.models import User
from app.utils.security import get_current_user  # 토큰에서 사용자 로드(예시 아래)

router = APIRouter(prefix="/api/v1/users", tags=["users"])

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