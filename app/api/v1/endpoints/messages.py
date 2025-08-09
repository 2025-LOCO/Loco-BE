from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_active_user
from app.crud.message import crud_message
from app.models.user import User
from app.schemas.message import Message, MessageCreate

router = APIRouter()

@router.post("/", response_model=Message)
def send_message(
    *,
    db: Session = Depends(get_db),
    message_in: MessageCreate,
    current_user: User = Depends(get_current_active_user),
):
    message = crud_message.create_with_sender(
        db, obj_in=message_in, sender_id=current_user.id
    )
    return message

@router.get("/conversation/{user_id}", response_model=List[Message])
def get_conversation(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    messages = crud_message.get_conversation(
        db, user1_id=current_user.id, user2_id=user_id
    )
    return messages