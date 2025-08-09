from typing import List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.message import Message
from app.schemas.message import MessageCreate, MessageBase

class CRUDMessage(CRUDBase[Message, MessageCreate, MessageBase]):
    def get_conversation(
        self, db: Session, *, user1_id: int, user2_id: int
    ) -> List[Message]:
        return db.query(Message).filter(
            ((Message.sender_id == user1_id) & (Message.receiver_id == user2_id)) |
            ((Message.sender_id == user2_id) & (Message.receiver_id == user1_id))
        ).order_by(Message.created_at).all()

    def create_with_sender(
        self, db: Session, *, obj_in: MessageCreate, sender_id: int
    ) -> Message:
        db_obj = Message(**obj_in.dict(), sender_id=sender_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

crud_message = CRUDMessage(Message)