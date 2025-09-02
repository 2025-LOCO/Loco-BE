# app/crud/user.py
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser:
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_by_nickname(self, db: Session, nickname: str) -> Optional[User]:
        return db.query(User).filter(User.nickname == nickname).first()

    def create(self, db: Session, user_in: UserCreate, hashed_pw: str) -> User:
        user = User(
            email=user_in.email,
            hashed_password=hashed_pw,
            nickname=user_in.nickname,
            intro=user_in.intro,
            city_id=user_in.city_id,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update(self, db: Session, user: User, user_in: UserUpdate) -> User:
        if user_in.nickname is not None:
            user.nickname = user_in.nickname
        if user_in.intro is not None:
            user.intro = user_in.intro
        if user_in.city_id is not None:
            user.city_id = user_in.city_id
        db.commit()
        db.refresh(user)
        return user

    def get_by_id(self, db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()


    def get_user_ranking(self, db: Session, user_id: int) -> Optional[int]:
        subquery = db.query(
            User.id,
            func.row_number().over(order_by=User.points.desc()).label('rank')
        ).subquery()
        result = db.query(subquery.c.rank).filter(subquery.c.id == user_id).first()
        return result[0] if result else None

    def get_best_users(self, db: Session, limit: int = 25) -> List[User]:
        return db.query(User).filter(User.ranking.isnot(None)).order_by(User.ranking.asc()).limit(limit).all()

    def get_new_local_users(self, db: Session, limit: int = 25) -> List[User]:
        return db.query(User).filter(User.is_local == True).order_by(User.created_at.desc()).limit(limit).all()

    def get_total_ranked_user_count(self, db: Session) -> int:
        return db.query(User).filter(User.ranking.isnot(None)).count()


crud_user = CRUDUser()