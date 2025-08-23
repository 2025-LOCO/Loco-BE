# app/api/v1/endpoints/votes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.vote import PlaceVoteCreate, RouteVoteCreate
from app.crud import vote as crud_vote
from app.models import User
from app.utils.security import get_current_user

router = APIRouter(prefix="/api/v1/votes", tags=["votes"])

@router.post("/places")
def vote_place(body: PlaceVoteCreate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    return crud_vote.vote_place(db, current.id, body.place_id, body.vote_type)

@router.post("/routes")
def vote_route(body: RouteVoteCreate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    return crud_vote.vote_route(db, current.id, body.route_id, body.vote_type)