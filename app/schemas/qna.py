# app/schemas/qna.py
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.vote_enums import VoteType

class QuestionCreate(BaseModel):
    title: str = Field(..., max_length=50)
    content: str

class QuestionOut(BaseModel):
    question_id: int
    user_id: int
    title: str
    content: str
    created_at: datetime
    view_count: int
    answer_count: int
    answers: List["AnswerOut"] = []
    user_nickname: str
    author_image_url: Optional[str] = None

    class Config:
        from_attributes = True

class AnswerCreate(BaseModel):
    question_id: int
    content: str
    like: Optional[VoteType] = None

class AnswerOut(BaseModel):
    answer_id: int
    user_id: int
    question_id: int
    content: str
    created_at: datetime
    user_nickname: str
    vote_type: Optional[VoteType] = None
    author_image_url: Optional[str] = None

    class Config:
        from_attributes = True