# app/api/v1/endpoints/regions.py
from fastapi import APIRouter, HTTPException, Query
from app.services import external_api

router = APIRouter(prefix="/regions", tags=["regions"])


@router.get("/sido", summary="시/도 목록 조회 (공공데이터포털)")
def get_sido_list():
    try:
        return external_api.get_regions_from_public_api()
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=502, detail=f"시/도 목록 조회 실패: {str(e)}")


@router.get("/sigungu", summary="시/군/구 목록 조회 (공공데이터포털)")
def get_sigungu_list(cd: str = Query(..., description="시/도 코드")):
    """
    공공데이터포털에서 특정 시/도의 시/군/구 목록을 가져옵니다.
    - cd: 시/도 코드 (예: '11'은 서울특별시)
    """
    try:
        return external_api.get_regions_from_public_api(sido_code=cd)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=502, detail=f"시/군/구 목록 조회 실패: {str(e)}")