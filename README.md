# Loco-BE

여행 맞춤 설문을 기반으로 루트를 추천하는 FastAPI 백엔드입니다.  
PostgreSQL + SQLAlchemy + Alembic, JWT 인증, bcrypt 해싱을 사용합니다.

## 요구 사항

- Python 3.11
- PostgreSQL 13+ (로컬: `localhost:5432`)
- OS X / Linux / WSL 권장

## 설치

```bash
python3.11 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 환경 변수 설정

루트 경로에 `.env` 파일을 생성합니다.

```env
# DB
DATABASE_URL=postgresql://postgres:mypassword@localhost:5432/travel_db

# JWT
JWT_SECRET=change-me-to-a-long-random-string

# (선택) 서버 설정
APP_HOST=127.0.0.1
APP_PORT=8000
```

## 데이터베이스 초기화

### 1) 데이터베이스 재생성(선택)
```bash
dropdb -U postgres travel_db
createdb -U postgres travel_db
```

### 2) Alembic 준비
```bash
alembic init alembic
```

(중요) 생성된 alembic/env.py 파일을 수정하여, 프로젝트의 .env 파일과 데이터베이스 모델을 직접 참조하도록 설정해야 합니다. (자세한 설정 코드는 프로젝트 내 alembic/env.py 파일 참조)

이렇게 하면 alembic.ini 파일에 데이터베이스 접속 정보를 직접 적을 필요 없이 안전하게 마이그레이션을 관리할 수 있습니다.

### (중요) pgvector 사용 시 리비전 파일 작성 규칙

리비전에 Vector 타입 컬럼이 포함되면, 해당 리비전 파일 상단과 upgrade() 초기에 아래를 반드시 추가하세요.

```python
# alembic/versions/xxxx_init_schema.py
from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector  # ★ 추가

def upgrade():
    # ★ DB 확장 설치 보장 (여러 번 실행되어도 안전)
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    # 예시: 벡터 컬럼 포함 테이블
    op.create_table(
        "place_embeddings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("embedding", Vector(768), nullable=True),  # ★ Vector 타입
    )
```

### 3) 마이그레이션 생성 및 적용
```bash
alembic revision --autogenerate -m "sync schema with new models"
alembic upgrade head
```

## 최소 시드(행정구역 코드)

```sql
INSERT INTO region_provinces (province_id, kor_name, eng_name)
VALUES ('11', '서울', 'Seoul')
ON CONFLICT (province_id) DO NOTHING;

INSERT INTO region_cities (region_id, province_id, kor_name, eng_name)
VALUES ('110000', '11', '서울특별시', 'Seoul')
ON CONFLICT (region_id) DO NOTHING;
```

## 서버 실행

```bash
uvicorn app.main:app --reload
```

Swagger UI: http://127.0.0.1:8000/docs  
ReDoc: http://127.0.0.1:8000/redoc

## 핵심 도메인

- User: 이메일/비밀번호(해시), 닉네임, 소개, 거주지 코드
- Place: 장소 정보
- Route: 맞춤 태그 기반 추천
- SurveySession: 설문 응답 저장

## 인증

### 회원가입 예시
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "test1@example.com",
  "nickname": "traveler1",
  "password": "mypassword123",
  "city_id": "110000"
}
```

### 로그인 예시
```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=test1@example.com&password=mypassword123
```

## 맞춤 설문 및 추천

### 설문 저장
```http
POST /api/v1/recommendations/survey
Authorization: Bearer <token>
Content-Type: application/json

{
  "period_days": 3,
  "env": "city",
  "with_whom": "friend",
  "move": "public",
  "atmosphere": "자유롭고 감성적인",
  "place_count": 3
}
```

### 추천 받기
```http
POST /api/v1/recommendations/routes
Content-Type: application/json

{
  "period_days": 2,
  "env": "sea",
  "with_whom": "love",
  "move": "car",
  "atmosphere": "아늑하고 로맨틱한",
  "place_count": 2
}
```

## 자주 발생하는 오류

- ModuleNotFoundError: No module named 'jwt' → `pip install PyJWT`
- ForeignKeyViolation (users.city_id) → `region_cities` 시드 필요
- Mapper 'User(users)' has no property 'trips' → Trip 모델 잔존 확인
- AttributeError: crud_user.get_by_email → CRUD 패턴 통일 필요

