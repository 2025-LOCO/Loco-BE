from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, regions, trips, locos, messages

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(regions.router, prefix="/regions", tags=["regions"])
api_router.include_router(trips.router, prefix="/trips", tags=["trips"])
api_router.include_router(locos.router, prefix="/locos", tags=["locos"])
api_router.include_router(messages.router, prefix="/messages", tags=["messages"])