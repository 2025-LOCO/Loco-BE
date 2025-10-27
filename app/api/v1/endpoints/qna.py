# app/api/v1/endpoints/qna.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app.core.database import get_db
from app.schemas.qna import QuestionCreate, QuestionOut, AnswerCreate, AnswerOut
from app.crud import qna as crud_qna
from app.models import User, Question, Answer
from app.utils.security import get_current_user

router = APIRouter(prefix="/qna", tags=["qna"])

@router.post("/questions", response_model=QuestionOut)
def create_question(body: QuestionCreate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    question = crud_qna.create_question(db, current.id, body)
    question.user_nickname = current.nickname
    question.author_image_url = current.image_url
    return question

@router.get("/questions", response_model=List[QuestionOut])
def list_questions(db: Session = Depends(get_db)):
    # crud_qna.list_questions()는 관계를 로드하지 않으므로, 여기서 직접 쿼리합니다.
    questions = db.query(Question).options(
        joinedload(Question.author),
        joinedload(Question.answers).joinedload(Answer.author)
    ).order_by(Question.question_id.desc()).all()
    
    # 스키마 유효성 검사를 위해 각 답변에 수동으로 user_nickname을 추가합니다.
    for q in questions:
        q.user_nickname = q.author.nickname if q.author else "탈퇴한 사용자"
        q.author_image_url = q.author.image_url if q.author else None
        for answer in q.answers:
            answer.user_nickname = answer.author.nickname if answer.author else "탈퇴한 사용자"
            answer.author_image_url = answer.author.image_url if answer.author else None
            
    return questions

@router.get("/questions/{question_id}", response_model=QuestionOut)
def read_question(question_id: int, db: Session = Depends(get_db)):
    q = db.query(Question).options(
        joinedload(Question.author),
        joinedload(Question.answers).joinedload(Answer.author)
    ).filter(Question.question_id == question_id).first()
    
    if not q:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
        
    # `AnswerOut` 스키마에 맞게 `user_nickname` 추가
    q.user_nickname = q.author.nickname if q.author else "탈퇴한 사용자"
    q.author_image_url = q.author.image_url if q.author else None
    for answer in q.answers:
        answer.user_nickname = answer.author.nickname if answer.author else "탈퇴한 사용자"
        answer.author_image_url = answer.author.image_url if answer.author else None
        
    return q

@router.post("/answers", response_model=AnswerOut)
def create_answer(body: AnswerCreate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    answer = crud_qna.create_answer(db, current.id, body)
    answer.user_nickname = current.nickname
    answer.author_image_url = current.image_url
    return answer