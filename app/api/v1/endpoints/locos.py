from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_active_user
from app.crud.loco import crud_loco
from app.models.user import User
from app.schemas.loco import Loco, LocoCreate, LocoUpdate

router = APIRouter()


@router.get("/", response_model=List[Loco])
def read_locos(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    locos = crud_loco.get_multi(db, skip=skip, limit=limit)
    return locos


@router.post("/", response_model=Loco)
def create_loco_profile(
        *,
        db: Session = Depends(get_db),
        loco_in: LocoCreate,
        current_user: User = Depends(get_current_active_user),
):
    # 이미 로코 프로필이 있는지 확인
    loco = crud_loco.get_by_user(db, user_id=current_user.id)
    if loco:
        raise HTTPException(status_code=400, detail="Loco profile already exists")

    loco = crud_loco.create_with_user(db, obj_in=loco_in, user_id=current_user.id)
    return loco


@router.get("/region/{region_id}", response_model=List[Loco])
def read_locos_by_region(
        region_id: int,
        db: Session = Depends(get_db)
):
    locos = crud_loco.get_by_region(db, region_id=region_id)
    return locos