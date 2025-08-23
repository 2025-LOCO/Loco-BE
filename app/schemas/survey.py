from typing import Optional
from pydantic import BaseModel, Field

# 설문 입력
class SurveyAnswer(BaseModel):
    # Q1: 기간 (일수), "한 달 살기", "장기 여행" 문자열도 허용하려면 별도 엔드포인트에서 전처리 가능
    period_days: Optional[int] = Field(None, ge=1, le=31)  # 1~31일
    is_one_month: Optional[bool] = False                   # 한 달 살기
    is_long_term: Optional[bool] = False                   # 장기 여행

    # Q2: 장소 선호
    env: Optional[str] = Field(None, pattern="^(sea|mountain|city|country)$")

    # Q3: 동행
    with_whom: Optional[str] = Field(None, pattern="^(alone|friend|love|family|pet)$")

    # Q4: 이동수단
    move: Optional[str] = Field(None, pattern="^(walk|bicycle|car|train|public)$")

    # Q5: 분위기
    atmosphere: Optional[str] = Field(
        None,
        pattern="^(잔잔하고 조용한|활기차고 신나는|아늑하고 로맨틱한|자유롭고 감성적인|자연과 함께하는)$"
    )

    # Q6: 하루 방문지 수
    place_count: Optional[int] = Field(None, ge=1, le=5)

class SurveySaved(BaseModel):
    survey_id: int

class RouteRecommendation(BaseModel):
    route_id: int
    name: str
    score: float
    matched: dict  # 어떤 태그가 매칭되었는지

    class Config:
        from_attributes = True