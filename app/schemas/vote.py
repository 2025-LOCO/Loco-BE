# app/schemas/vote.py
from pydantic import BaseModel
from app.models.vote_enums import VoteType

class PlaceVoteCreate(BaseModel):
    place_id: int
    vote_type: VoteType

class RouteVoteCreate(BaseModel):
    route_id: int
    vote_type: VoteType