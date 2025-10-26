# app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

from app.core.database import get_db
from app.schemas.user import UserCreate, UserOut
from app.schemas.auth import Token
from app.crud.user import crud_user
from app.utils.jwt import create_access_token  # 아래에 예시 제공
from app.utils.security import get_current_user
from app.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    if crud_user.get_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    # 닉네임 중복 체크
    if crud_user.get_by_nickname(db, user_in.nickname):
        raise HTTPException(status_code=400, detail="Nickname already taken")
    hashed_pw = pwd_context.hash(user_in.password)
    user = crud_user.create(db, user_in, hashed_pw)
    return user

# 기존 OAuth2PasswordRequestForm(username/password) 흐름을 유지
@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    u = crud_user.get_by_email(db, form.username)
    if not u or not pwd_context.verify(form.password, u.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    token = create_access_token({"sub": str(u.id), "ver": u.token_version})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": u.id,
        "user_nickname": u.nickname,
    }

@router.post("/logout", status_code=200, summary="로그아웃")
def logout(db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    current.token_version += 1
    db.add(current)
    db.commit()
    return {"detail": "Logged out from all sessions."}