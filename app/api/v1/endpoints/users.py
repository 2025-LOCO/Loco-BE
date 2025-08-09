from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_active_user
from app.crud.user import crud_user
from app.models.user import User
from app.schemas.user import User as UserSchema, UserUpdate

router = APIRouter()

@router.get("/me", response_model=UserSchema)
def read_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.put("/me", response_model=UserSchema)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
):
    user = crud_user.update(db, db_obj=current_user, obj_in=user_in)
    return user

@router.get("/{user_id}", response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user