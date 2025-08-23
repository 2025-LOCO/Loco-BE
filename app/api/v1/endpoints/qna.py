# app/api/v1/endpoints/qna.py
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.qna import QuestionCreate, QuestionOut, AnswerCreate, AnswerOut
from app.crud import qna as crud_qna
from app.models import User
from app.utils.security import get_current_user

router = APIRouter(prefix="/api/v1/qna", tags=["qna"])

@router.post("/questions", response_model=QuestionOut)
def create_question(body: QuestionCreate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    return crud_qna.create_question(db, current.id, body)

@router.get("/questions", response_model=List[QuestionOut])
def list_questions(db: Session = Depends(get_db)):
    return crud_qna.list_questions(db)

@router.post("/answers", response_model=AnswerOut)
def create_answer(body: AnswerCreate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    return crud_qna.create_answer(db, current.id, body)