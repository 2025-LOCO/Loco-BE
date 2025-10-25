from sqlalchemy.orm import Session
from typing import Optional
from app.models.survey import SurveySession
from app.schemas.survey import SurveyAnswer

def _normalize_period(ans: SurveyAnswer) -> Optional[int]:
    if not ans.period:
        return None
    period_map = {
        "당일치기": 1,
        "1박2일": 2,
        "2박3일": 3,
        "3박4일": 4,
        "장기여행": 33,
    }
    return period_map.get(ans.period)

def create_survey(db: Session, user_id: Optional[int], ans: SurveyAnswer) -> SurveySession:
    obj = SurveySession(
        user_id=user_id,
        period=_normalize_period(ans),
        env=ans.env,
        with_whom=ans.with_whom,
        move=ans.move,
        atmosphere=ans.atmosphere,
        place_count=ans.place_count,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj