# app/schemas/auth.py
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    user_nickname: str

class LoginRequest(BaseModel):
    email: str
    password: str