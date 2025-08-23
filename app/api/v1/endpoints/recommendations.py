from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.survey import SurveyAnswer, SurveySaved, RouteRecommendation
from app.crud.survey import create_survey
from app.services.recommend import recommend_routes
from app.models import User
from app.utils.security import get_current_user  # 로그인 사용자 기반 저장이 필요할 때

router = APIRouter(prefix="/api/v1/recommendations", tags=["recommendations"])

@router.post("/survey", response_model=SurveySaved)
def submit_survey(
    payload: SurveyAnswer,
    db: Session = Depends(get_db),
    current: User = Depends(get_current_user)  # 익명 허용하려면 Optional 처리로 바꾸세요.
):
    s = create_survey(db, user_id=current.id if current else None, ans=payload)
    return {"survey_id": s.id}

@router.post("/routes", response_model=List[RouteRecommendation])
def get_recommended_routes(
    payload: SurveyAnswer,  # 설문과 동일 포맷으로 바로 추천만 받고 싶을 때
    db: Session = Depends(get_db)
):
    results = recommend_routes(db, payload, limit=10)
    return [
        RouteRecommendation(
            route_id=r["route"].route_id,
            name=r["route"].name,
            score=r["score"],
            matched=r["matched"],
        )
        for r in results
    ]