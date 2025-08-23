# app/utils/jwt.py
import os, time, jwt  # pyjwt
SECRET_KEY = os.getenv("JWT_SECRET", "dev-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 60 * 60 * 24  # 24h

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode["exp"] = int(time.time()) + ACCESS_TOKEN_EXPIRE_SECONDS
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)