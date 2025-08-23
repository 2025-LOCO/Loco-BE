# app/api/v1/endpoints/routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.route import RouteCreate, RouteOut
from app.crud import route as crud_route
from app.models import User
from app.utils.security import get_current_user

router = APIRouter(prefix="/api/v1/routes", tags=["routes"])

@router.post("", response_model=RouteOut)
def create_route(body: RouteCreate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    return crud_route.create(db, user_id=current.id, obj_in=body)

@router.get("", response_model=List[RouteOut])
def list_routes(db: Session = Depends(get_db)):
    return crud_route.list_all(db)