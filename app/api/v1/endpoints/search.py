# app/api/v1/endpoints/search.py

from fastapi import APIRouter, HTTPException, Query
from app.services import external_api

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/tourism")
def search_tourism(keyword: str = Query(..., min_length=2, description="검색할 키워드")):
    result = external_api.search_tourism_by_keyword(keyword)
    if result is None:
        raise HTTPException(status_code=503, detail="외부 API를 호출하는 데 실패했습니다.")
    return result


@router.get("/places")
def search_places(keyword: str = Query(..., min_length=2, description="검색할 키워드")):
    result = external_api.search_kakao_places_by_keyword(keyword)
    if result is None:
        raise HTTPException(status_code=503, detail="외부 API를 호출하는 데 실패했습니다.")
    return result