# app/services/recommend.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import Route, User
from app.schemas.survey import SurveyAnswer
from app.services.vector_service import text_to_vector


def recommend_routes_by_vector(db: Session, ans: SurveyAnswer, limit: int = 10):
    # 여행자가 선택한 태그를 하나의 문장으로 조합
    request_text = f"{ans.env or ''} {ans.with_whom or ''} {ans.atmosphere or ''}"

    if not request_text.strip():
        return []

    # 이 문장을 '요청 벡터'로 변환
    request_vector = text_to_vector(request_text)

    # DB에 단 한 번의 쿼리로 추천 결과를 요청
    stmt = (
        select(Route)
        .join(User, Route.created_by == User.id)  # 현지인인지 확인하기 위해 User 테이블 조인
        .where(User.is_local == True)  # 현지인이 만든 루트만
        .order_by(Route.embedding.cosine_distance(request_vector))  # '요청 벡터'와 가장 유사한 순서로 정렬
        .limit(limit)
    )

    results = db.scalars(stmt).all()
    return results
