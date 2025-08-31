# alembic/env.py
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# 이 프로젝트의 Base/메타데이터를 가져온다
# 주의: 모든 모델이 app.models.__init__ 에서 import/export 되어 있어야 함
from app.core.database import Base
from app.models import *  # noqa: F401 - 메타데이터 로딩 목적
from app.core.config import settings  # DATABASE_URL 제공하는 모듈

# 이곳은 Alembic의 config 객체 (alembic.ini)
config = context.config

# .ini 로거 설정
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Alembic이 참조할 메타데이터
target_metadata = Base.metadata

def get_url():
    # DATABASE_URL을 환경 또는 settings에서 가져옵니다.
    # 예: postgresql+psycopg2://user:pass@host:5432/dbname
    return settings.DATABASE_URL

def run_migrations_offline():
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,     # 타입 변경 감지
        compare_server_default=True,  # server_default 변경 감지
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