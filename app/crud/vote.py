# app/crud/vote.py
from sqlalchemy.orm import Session
from app.models import PlaceVote, RouteVote, Place, Route
from app.models.vote_enums import VoteType

def vote_place(db: Session, user_id: int, place_id: int, vote: VoteType) -> PlaceVote:
    pv = db.query(PlaceVote).filter_by(user_id=user_id, place_id=place_id).first()
    if pv:
        pv.vote_type = vote
    else:
        pv = PlaceVote(user_id=user_id, place_id=place_id, vote_type=vote)
        db.add(pv)
    db.flush()
    # 집계 재계산
    place = db.get(Place, place_id)
    place.count_real = db.query(PlaceVote).filter_by(place_id=place_id, vote_type=VoteType.real).count()
    place.count_normal = db.query(PlaceVote).filter_by(place_id=place_id, vote_type=VoteType.normal).count()
    place.count_bad = db.query(PlaceVote).filter_by(place_id=place_id, vote_type=VoteType.bad).count()
    db.commit()
    db.refresh(pv)
    return pv

def vote_route(db: Session, user_id: int, route_id: int, vote: VoteType) -> RouteVote:
    rv = db.query(RouteVote).filter_by(user_id=user_id, route_id=route_id).first()
    if rv:
        rv.vote_type = vote
    else:
        rv = RouteVote(user_id=user_id, route_id=route_id, vote_type=vote)
        db.add(rv)
    db.flush()
    route = db.get(Route, route_id)
    route.count_real = db.query(RouteVote).filter_by(route_id=route_id, vote_type=VoteType.real).count()
    route.count_normal = db.query(RouteVote).filter_by(route_id=route_id, vote_type=VoteType.normal).count()
    route.count_bad = db.query(RouteVote).filter_by(route_id=route_id, vote_type=VoteType.bad).count()
    db.commit()
    db.refresh(rv)
    return rv