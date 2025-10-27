# app/utils/security.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import jwt
from app.core.database import get_db
from app.models import User
from app.utils.jwt import SECRET_KEY, ALGORITHM

bearer = HTTPBearer(bearerFormat="JWT", scheme_name="Authorization")

def get_current_user(cred: HTTPAuthorizationCredentials = Depends(bearer),
                     db: Session = Depends(get_db)) -> User:
    token = cred.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        uid = int(payload.get("sub"))
        token_ver = payload.get("ver", 0)  # 하위 호환: 없으면 0
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = db.get(User, uid)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    # 토큰 버전과 현재 사용자 버전이 다르면 무효화
    if token_ver != user.token_version:
        raise HTTPException(status_code=401, detail="Token has been revoked")

    return user


def get_optional_current_user(
    cred: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)
) -> User | None:
    if not cred:
        return None
    try:
        user = get_current_user(cred, db)
        return user
    except HTTPException:
        return None