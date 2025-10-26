# app/services/external_api.py
import ssl
import certifi
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from fastapi import HTTPException
from xml.etree import ElementTree as ET

from app.core.config import settings

TOUR_API_BASE = "https://apis.data.go.kr/B551011/KorService2/searchKeyword2"
KAKAO_LOCAL_API_BASE = "https://dapi.kakao.com/v2/local/search/keyword.json"

SGIS_AUTH_HOST = "https://sgisapi.kostat.go.kr/OpenAPI3/auth/authentication.json"
SGIS_API_HOST = "https://sgisapi.kostat.go.kr/OpenAPI3/addr/stage.json"

_sgis_token_cache = {
    "token": None,
    "expiry": 0  # 토큰 만료 시간 (timestamp)
}

class LegacySSLAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self._context = ssl.create_default_context(cafile=certifi.where())
        # TLS 1.2 이상
        if hasattr(ssl, "TLSVersion"):
            self._context.minimum_version = ssl.TLSVersion.TLSv1_2
        # 레거시 장비 호환
        if hasattr(ssl, "OP_LEGACY_SERVER_CONNECT"):
            self._context.options |= ssl.OP_LEGACY_SERVER_CONNECT
        try:
            self._context.set_ciphers("DEFAULT:@SECLEVEL=1")
        except ssl.SSLError:
            pass
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        kwargs["ssl_context"] = self._context
        return super().init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        kwargs["ssl_context"] = self._context
        return super().proxy_manager_for(*args, **kwargs)

# 세션 구성
base_retries = Retry(
    total=3,
    backoff_factor=0.3,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
)
session = requests.Session()
session.mount("https://", HTTPAdapter(max_retries=base_retries))
session.mount("https://apis.data.go.kr", LegacySSLAdapter(max_retries=base_retries))

def _parse_tourapi_response(resp: requests.Response):
    """
    TourAPI 응답을 안전하게 파싱:
    1) JSON 시도
    2) 실패 시 XML에서 resultCode/resultMsg 추출
    3) 그래도 실패면 원문 일부를 포함해 HTTPException
    """
    # 우선 상태코드 확인(200이 아니어도 본문에 오류 메시지가 있을 수 있음)
    text_preview = (resp.text or "")[:800]  # 미리보기(로그/에러에 포함)
    ctype = (resp.headers.get("Content-Type") or "").lower()

    # JSON 우선
    if "json" in ctype:
        try:
            return resp.json()
        except Exception as e:
            # JSON Content-Type인데도 파싱 실패 → 본문 확인 목적의 에러
            raise HTTPException(
                status_code=502,
                detail={
                    "message": "TourAPI JSON 파싱 실패",
                    "error": str(e),
                    "content_type": ctype,
                    "status_code": resp.status_code,
                    "preview": text_preview,
                },
            )

    # JSON이 아니면 XML 시도(에러/권한 문제일 가능성 높음)
    try:
        root = ET.fromstring(resp.content)
        # 공공데이터포털 공통 응답 포맷 추정
        result_code = root.findtext(".//resultCode")
        result_msg = root.findtext(".//resultMsg")
        # 정상 결과인 경우도 XML일 수 있으나, 보통 에러는 resultCode 존재
        if result_code or result_msg:
            raise HTTPException(
                status_code=502,
                detail={
                    "message": "TourAPI가 XML 에러로 응답",
                    "resultCode": result_code,
                    "resultMsg": result_msg,
                    "status_code": resp.status_code,
                },
            )
        # resultCode가 없으면 데이터 XML일 수 있음 → 필요시 XML 파서 추가 구현
        raise HTTPException(
            status_code=502,
            detail={
                "message": "TourAPI가 JSON이 아닌 응답을 반환",
                "content_type": ctype,
                "status_code": resp.status_code,
                "preview": text_preview,
            },
        )
    except ET.ParseError:
        # XML로도 해석 불가 → HTML/빈 응답 등
        raise HTTPException(
            status_code=502,
            detail={
                "message": "TourAPI 응답 형식 알 수 없음(JSON/XML 아님)",
                "content_type": ctype,
                "status_code": resp.status_code,
                "preview": text_preview,
            },
        )


def _get_sgis_token() -> str:
    """
    SGIS 인증 토큰을 가져오거나 갱신합니다. (기존 session 객체 사용)
    """
    global _sgis_token_cache
    now = int(time.time())

    # 1. 캐시된 토큰이 유효하면 반환
    if _sgis_token_cache["token"] and _sgis_token_cache["expiry"] > now:
        return _sgis_token_cache["token"]

    # 2. SGIS 키가 설정되어 있는지 확인
    key = getattr(settings, "SGIS_CONSUMER_KEY", None)
    secret = getattr(settings, "SGIS_CONSUMER_SECRET", None)
    if not key or not secret:
        raise HTTPException(status_code=503, detail="SGIS API 키(SGIS_CONSUMER_KEY)가 설정되지 않았습니다.")

    try:
        # 3. 새 토큰 요청 (기존 session 사용)
        params = {"consumer_key": key, "consumer_secret": secret}
        resp = session.get(SGIS_AUTH_HOST, params=params, timeout=5)
        resp.raise_for_status()  # 200 OK가 아니면 예외 발생
        data = resp.json()

        access_token = data.get("result", {}).get("accessToken")
        if not access_token:
            raise HTTPException(status_code=502, detail="SGIS 토큰 발급 응답 형식이 올바르지 않습니다.")

        # 4. 캐시 저장 (SGIS 토큰은 2시간 유효, 1시간 50분(6600초)으로 설정)
        _sgis_token_cache["token"] = access_token
        _sgis_token_cache["expiry"] = now + 6600

        return access_token
    except Exception as e:
        # 5. 실패 시 캐시 비우기
        _sgis_token_cache["token"] = None
        _sgis_token_cache["expiry"] = 0
        raise HTTPException(status_code=502, detail=f"SGIS 토큰 발급 실패: {str(e)}")


def get_sgis_sido():
    """SGIS 시/도 목록 조회"""
    token = _get_sgis_token()
    params = {"accessToken": token}
    resp = session.get(SGIS_API_HOST, params=params, timeout=5)
    resp.raise_for_status()
    return resp.json()


def get_sgis_sigungu(sido_code: str):
    """SGIS 시/군/구 목록 조회"""
    token = _get_sgis_token()
    params = {"accessToken": token, "cd": sido_code}
    resp = session.get(SGIS_API_HOST, params=params, timeout=5)
    resp.raise_for_status()
    return resp.json()

def search_tourism_by_keyword(keyword: str):
    tour_key = getattr(settings, "TOUR_API_KEY", None)
    if not tour_key:
        raise HTTPException(status_code=503, detail="TourAPI 키(TOUR_API_KEY)가 설정되어 있지 않습니다.")

    params = {
        "serviceKey": tour_key,      # 반드시 디코딩된 '원문' 키
        "MobileOS": "ETC",
        "MobileApp": "LocoService",
        "keyword": keyword,
        "arrange": "A",
        "_type": "json",
        "numOfRows": 10,
        "pageNo": 1,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; LocoService/1.0)",
        "Accept": "application/json",   # JSON 선호 명시
    }

    resp = session.get(TOUR_API_BASE, params=params, headers=headers, timeout=10)

    # 상태코드가 400/500이어도 본문에 에러 설명이 있으므로 raise_for_status 전에 파싱 시도
    if resp.status_code != 200:
        # 본문에서 에러 메세지 추출 시도
        return _parse_tourapi_response(resp)

    # 200인 경우에도 XML/HTML일 수 있으니 안전 파싱
    return _parse_tourapi_response(resp)

def search_kakao_places_by_keyword(keyword: str):
    headers = {
        "Authorization": f"KakaoAK {settings.KAKAO_REST_API_KEY}",
        "User-Agent": "Mozilla/5.0 (compatible; LocoService/1.0)",
        "Accept": "application/json",
    }
    params = {"query": keyword, "page": 1, "size": 10}
    resp = session.get(KAKAO_LOCAL_API_BASE, headers=headers, params=params, timeout=5)
    resp.raise_for_status()
    return resp.json()
