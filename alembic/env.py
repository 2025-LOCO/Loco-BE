import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from dotenv import load_dotenv

# --- FastAPI 프로젝트 경로 설정 ---
# alembic.ini가 있는 루트 디렉토리를 sys.path에 추가
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

# --- FastAPI 모델 및 설정 로드 ---
from app.core.database import Base
from app.core.config import settings
# 모든 모델을 Base.metadata에 등록하기 위해 임포트
from app.models import *

# .env 파일 로드 (DATABASE_URL을 읽기 위함)
load_dotenv()

# Alembic Config 객체, .ini 파일의 값에 접근 가능
config = context.config

# .ini 파일에 설정된 sqlalchemy.url을 FastAPI 설정값으로 덮어쓰기
# .env 파일에 정의된 DATABASE_URL을 사용하게 됨
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)


# Python 로깅을 위한 .ini 파일 해석
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# autogenerate를 지원하기 위해 모델의 MetaData 객체를 설정
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """'offline' 모드에서 마이그레이션을 실행합니다.
    데이터베이스 연결 없이 SQL 스크립트를 생성합니다.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """'online' 모드에서 마이그레이션을 실행합니다.
    데이터베이스에 연결하여 DDL 명령을 직접 실행합니다.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()