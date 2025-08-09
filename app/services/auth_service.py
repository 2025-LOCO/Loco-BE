from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.core.security import create_access_token, verify_password, get_password_hash
from app.core.config import settings
from app.crud.user import crud_user
from app.models.user import User
from app.schemas.user import UserCreate


class AuthService:
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """사용자 인증"""
        user = crud_user.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def create_access_token_for_user(user: User) -> dict:
        """사용자를 위한 액세스 토큰 생성"""
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "is_loco": user.is_loco
            }
        }

    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> User:
        """새 사용자 등록"""
        # 이메일 중복 확인
        if crud_user.get_by_email(db, email=user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # 사용자명 중복 확인
        if crud_user.get_by_username(db, username=user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )

        # 사용자 생성
        user = crud_user.create(db, obj_in=user_data)
        return user

    @staticmethod
    def change_password(db: Session, user: User, current_password: str, new_password: str) -> bool:
        """비밀번호 변경"""
        if not verify_password(current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect current password"
            )

        user.hashed_password = get_password_hash(new_password)
        db.add(user)
        db.commit()
        return True


auth_service = AuthService()