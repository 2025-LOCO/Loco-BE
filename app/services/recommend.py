from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models import Route
from app.schemas.survey import SurveyAnswer
from app.crud.survey import _normalize_period

WEIGHTS = {
    "period": 1.0,
    "env": 1.5,
    "with_whom": 1.2,
    "move": 1.0,
    "atmosphere": 1.0,
    "place_count": 0.8,
}

def _collect_filters(ans: SurveyAnswer):
    """하드 필터(좁히기). period는 유연 매칭을 위해 하드 필터에서 제외해도 됨."""
    filters = []
    if ans.env:
        filters.append(Route.tag_env == ans.env)
    if ans.with_whom:
        filters.append(Route.tag_with == ans.with_whom)
    if ans.move:
        filters.append(Route.tag_move == ans.move)
    if ans.atmosphere:
        filters.append(Route.tag_atmosphere == ans.atmosphere)
    if ans.place_count:
        filters.append(Route.tag_place_count == ans.place_count)
    return filters

def _score_route(route: Route, ans: SurveyAnswer) -> Tuple[float, Dict]:
    score = 0.0
    matched = {}

    # period(유연): 정확히 같으면 가점
    norm_period = _normalize_period(ans)
    if norm_period is not None and route.tag_period is not None:
        if route.tag_period == norm_period:
            score += WEIGHTS["period"]
            matched["period"] = True

    # env
    if ans.env and route.tag_env == ans.env:
        score += WEIGHTS["env"]; matched["env"] = True

    # with_whom
    if ans.with_whom and route.tag_with == ans.with_whom:
        score += WEIGHTS["with_whom"]; matched["with_whom"] = True

    # move
    if ans.move and route.tag_move == ans.move:
        score += WEIGHTS["move"]; matched["move"] = True

    # atmosphere
    if ans.atmosphere and route.tag_atmosphere == ans.atmosphere:
        score += WEIGHTS["atmosphere"]; matched["atmosphere"] = True

    # place_count
    if ans.place_count and route.tag_place_count == ans.place_count:
        score += WEIGHTS["place_count"]; matched["place_count"] = True

    # 인기 반영(선택): 반응 카운트의 가중치
    popularity = (route.count_real * 1.0 + route.count_normal * 0.3 - route.count_bad * 0.5)
    score += 0.1 * popularity

    return score, matched

def recommend_routes(db: Session, ans: SurveyAnswer, limit: int = 10):
    # 1) 하드 필터로 1차 좁히기 (없으면 전체 대상)
    filters = _collect_filters(ans)
    q = db.query(Route)
    if filters:
        q = q.filter(and_(*filters))

    candidates = q.limit(200).all()  # 과도한 연산 방지용 상한

    # 2) 스코어링
    scored = []
    for r in candidates:
        s, matched = _score_route(r, ans)
        scored.append((s, r, matched))

    # 3) 점수순 정렬
    scored.sort(key=lambda x: x[0], reverse=True)

    # 4) 상위 N건 반환
    results = []
    for s, r, m in scored[:limit]:
        results.append({"route": r, "score": float(s), "matched": m})
    return results