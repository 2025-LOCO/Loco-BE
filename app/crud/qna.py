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
    a = Answer(
        user_id=user_id,
        question_id=obj_in.question_id,
        content=obj_in.content,
        vote_type=obj_in.like
    )
    db.add(a)
    # answer_count 증가
    db.flush()
    q = db.get(Question, obj_in.question_id)
    q.answer_count = (q.answer_count or 0) + 1
    db.commit()
    db.refresh(a)
    return a

def count_answers_by_user(db: Session, user_id: int) -> int:
    return db.query(Answer).filter(Answer.user_id == user_id).count()

def delete_question(db: Session, question_id: int, user_id: int) -> Question | None:
    question = db.query(Question).filter(Question.question_id == question_id).first()
    if not question:
        return None  # 존재하지 않음
    if question.user_id != user_id:
        return None  # 권한 없음
    
    db.delete(question)
    db.commit()
    return question

def delete_answer(db: Session, answer_id: int, user_id: int) -> Answer | None:
    answer = db.query(Answer).filter(Answer.answer_id == answer_id).first()
    if not answer:
        return None # 존재하지 않음
    if answer.user_id != user_id:
        return None # 권한 없음

    # 답변 수 카운트 감소
    question = db.query(Question).filter(Question.question_id == answer.question_id).first()
    if question:
        question.answer_count = max(0, question.answer_count - 1)

    db.delete(answer)
    db.commit()
    return answer