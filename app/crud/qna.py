# app/crud/qna.py
from sqlalchemy.orm import Session
from typing import List
from app.models import Question, Answer
from app.schemas.qna import QuestionCreate, AnswerCreate

def create_question(db: Session, user_id: int, obj_in: QuestionCreate) -> Question:
    q = Question(user_id=user_id, title=obj_in.title, content=obj_in.content)
    db.add(q)
    db.commit()
    db.refresh(q)
    return q

def list_questions(db: Session, limit: int = 50, offset: int = 0) -> List[Question]:
    return db.query(Question).order_by(Question.question_id.desc()).offset(offset).limit(limit).all()

def create_answer(db: Session, user_id: int, obj_in: AnswerCreate) -> Answer:
    a = Answer(user_id=user_id, question_id=obj_in.question_id, content=obj_in.content)
    db.add(a)
    # answer_count 증가
    db.flush()
    q = db.get(Question, obj_in.question_id)
    q.answer_count = (q.answer_count or 0) + 1
    db.commit()
    db.refresh(a)
    return a