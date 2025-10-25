from typing import Optional
from pydantic import BaseModel, Field

# 설문 입력
class SurveyAnswer(BaseModel):
    # Q1: 기간
    period: Optional[str] = Field(None, pattern="^(당일치기|1박2일|2박3일|3박4일|장기여행)$")

    # Q2: 장소 선호
    env: Optional[str] = Field(None, pattern="^(바다|산|도시|농촌)$")

    # Q3: 동행
    with_whom: Optional[str] = Field(None, pattern="^(혼자|친구|연인|가족|반려동물)$")

    # Q4: 이동수단
    move: Optional[str] = Field(None, pattern="^(걸어서|자전거|자동차|기차|버스)$")

    # Q5: 분위기
    atmosphere: Optional[str] = Field(
        None,
        pattern="^(잔잔하고 조용한|신나는 액티비티|다채로운 경험|맛있는 여행|아늑하고 로맨틱한)$"
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