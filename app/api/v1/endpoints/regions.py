from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.region import crud_region
from app.schemas.region import Region

router = APIRouter()

@router.get("/", response_model=List[Region])
def read_regions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    regions = crud_region.get_multi(db, skip=skip, limit=limit)
    return regions

@router.get("/level/{level}", response_model=List[Region])
def read_regions_by_level(
    level: int,
    db: Session = Depends(get_db)
):
    regions = crud_region.get_by_level(db, level=level)
    return regions

@router.get("/parent/{parent_code}", response_model=List[Region])
def read_sub_regions(
    parent_code: str,
    db: Session = Depends(get_db)
):
    regions = crud_region.get_by_parent_code(db, parent_code=parent_code)
    return regions