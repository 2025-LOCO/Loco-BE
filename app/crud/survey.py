from sqlalchemy.orm import Session
from typing import Optional
from app.models.survey import SurveySession
from app.schemas.survey import SurveyAnswer

def _normalize_period(ans: SurveyAnswer) -> Optional[int]:
    if ans.is_long_term:
        return 33
    if ans.is_one_month:
        return 32
    if ans.period_days:
        return ans.period_days
    return None

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