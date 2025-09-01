# alembic/env.py
from __future__ import annotations
import os, sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# 1) 프로젝트 루트 경로 추가 (alembic/ 상위가 루트라고 가정)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 2) 앱 메타데이터 로드
from app.core.database import Base           # Base.metadata
from app.core.config import settings         # DATABASE_URL 제공
# models/__init__.py 안에서 모든 모델을 import/export 하고 있어야 자동 감지됩니다.
from app import models  # noqa: F401

config = context.config

# 로깅
if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def _normalize_url(url: str | None) -> str:
    """
    Alembic용 동기 URL을 반환합니다.
    앱이 async URL을 사용할 경우 psycopg2로 변환합니다.
    """
    if not url:
        # alembic.ini의 sqlalchemy.url 로 폴백
        return config.get_main_option("sqlalchemy.url")

    if url.startswith("postgresql+asyncpg://"):
        return "postgresql+psycopg2://" + url.split("://", 1)[1]
    return url

def get_url() -> str:
    # 우선순위: 환경변수 > settings.DATABASE_URL > alembic.ini
    env_url = os.getenv("DATABASE_URL")
    url = env_url or getattr(settings, "DATABASE_URL", None)
    norm = _normalize_url(url)
    if not norm:
        raise RuntimeError(
            "DATABASE_URL이 비어 있습니다. 환경변수 또는 alembic.ini(sqlalchemy.url)를 설정하세요."
        )
    return norm

def run_migrations_offline():
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()