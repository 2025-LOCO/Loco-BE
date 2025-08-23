# app/schemas/qna.py
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

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

    class Config:
        from_attributes = True

class AnswerCreate(BaseModel):
    question_id: int
    content: str

class AnswerOut(BaseModel):
    answer_id: int
    user_id: int
    question_id: int
    content: str
    created_at: datetime

    class Config:
        from_attributes = True