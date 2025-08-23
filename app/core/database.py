# app/core/database.py
from __future__ import annotations

import os
from typing import Generator

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker

# 제약/인덱스 네이밍 규칙(권장: Alembic autogenerate 안정성↑)
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
metadata = MetaData(naming_convention=NAMING_CONVENTION)
Base = declarative_base(metadata=metadata)

# DATABASE_URL 가져오기
# app.core.config.settings.DATABASE_URL 을 쓰고 있다면 우선 시도하고,
# 없으면 환경변수로 fallback 합니다.
DATABASE_URL = None
try:
    from app.core.config import settings  # 존재하지 않으면 except로
    DATABASE_URL = getattr(settings, "DATABASE_URL", None)
except Exception:
    pass

if not DATABASE_URL:
    DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL이 설정되어 있지 않습니다.")

# Engine / Session
engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)

def get_db() -> Generator:
    """
    FastAPI 의존성에서 사용되는 DB 세션 제공자.
    사용 예: def endpoint(db: Session = Depends(get_db)): ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()