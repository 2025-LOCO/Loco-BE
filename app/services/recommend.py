# app/services/recommend.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import Route, User
from app.schemas.survey import SurveyAnswer
from app.services.vector_service import text_to_vector


def recommend_routes(db: Session, ans: SurveyAnswer, limit: int = 10):
    """
    설문 답변을 기반으로 유사도가 높은 루트와 점수를 함께 반환합니다.
    """
    request_text = f"{ans.env or ''} {ans.with_whom or ''} {ans.atmosphere or ''}"

    if not request_text.strip():
        return []

    request_vector = text_to_vector(request_text)

    # 유사도 점수(distance)를 함께 조회합니다. (거리가 가까울수록 유사도가 높음)
    distance = Route.embedding.cosine_distance(request_vector)
    stmt = (
        select(Route, distance.label("distance"))
        .join(User, Route.created_by == User.id)
        .where(User.is_local == True)
        .order_by(distance) # 거리가 가까운 순으로 정렬
        .limit(limit)
    )

    # (Route, distance) 튜플 형태로 결과를 받습니다.
    results = db.execute(stmt).all()

    # API가 기대하는 딕셔너리 형태로 가공하여 반환합니다.
    return [
        {
            "route": row.Route,
            "score": 1 - row.distance,  # 거리를 점수(0~1)로 변환 (1에 가까울수록 유사)
            "matched": {}  # 현재는 비워둠
        }
        for row in results
    ]
