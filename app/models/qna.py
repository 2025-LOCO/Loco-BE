from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from app.core.database import Base
from app.models.vote_enums import VoteType

class Question(Base):
    __tablename__ = "questions"

    question_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    title: Mapped[str] = mapped_column(String(50))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    view_count: Mapped[int] = mapped_column(Integer, default=0)
    answer_count: Mapped[int] = mapped_column(Integer, default=0)

    author = relationship("User", back_populates="questions")
    answers = relationship("Answer", back_populates="question", cascade="all, delete-orphan")


class Answer(Base):
    __tablename__ = "answers"

    answer_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(Text)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.question_id"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # 답변 반응 (선택)
    vote_type: Mapped[Optional[VoteType]] = mapped_column(Enum(VoteType), nullable=True)

    author = relationship("User", back_populates="answers")
    question = relationship("Question", back_populates="answers")