# app/utils/jwt.py
import os, time, jwt  # pyjwt
SECRET_KEY = os.getenv("JWT_SECRET", "dev-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 60 * 30  # 30m

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    # ver(토큰 버전) 없으면 0으로 넣어 하위 호환
    if "ver" not in to_encode:
        to_encode["ver"] = 0
    to_encode["exp"] = int(time.time()) + ACCESS_TOKEN_EXPIRE_SECONDS
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)