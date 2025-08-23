# app/api/v1/api.py
from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, places, routes, favorites, votes, qna, recommendations

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(places.router)
api_router.include_router(routes.router)
api_router.include_router(favorites.router)
api_router.include_router(votes.router)
api_router.include_router(qna.router)
api_router.include_router(recommendations.router)