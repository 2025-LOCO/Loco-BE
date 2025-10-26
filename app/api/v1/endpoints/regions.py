# app/api/v1/endpoints/regions.py
from fastapi import APIRouter, HTTPException, Query
from app.services import external_api

router = APIRouter(prefix="/regions", tags=["regions"])

@router.get("/sido", summary="시/도 목록 조회 (SGIS)")
def get_sido_list():
    try:
        # services.external_api에 추가한 함수 호출
        return external_api.get_sgis_sido()
    except Exception as e:
        # 서비스에서 발생한 HTTPException을 그대로 반환하거나 새로 생성
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=502, detail=f"SGIS 시/도 목록 조회 실패: {str(e)}")

@router.get("/sigungu", summary="시/군/구 목록 조회 (SGIS)")
def get_sigungu_list(cd: str = Query(..., description="시/도 코드 (sido_code)")):
    """
    SGIS에서 특정 시/도의 시/군/구 목록을 가져옵니다.
    - cd: 시/도 코드 (예: '11'은 서울특별시)
    """
    try:
        # services.external_api에 추가한 함수 호출
        return external_api.get_sgis_sigungu(sido_code=cd)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=502, detail=f"SGIS 시/군/구 목록 조회 실패: {str(e)}")