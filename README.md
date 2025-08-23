# Loco-BE

여행 맞춤 설문을 기반으로 루트를 추천하는 FastAPI 백엔드입니다.  
PostgreSQL + SQLAlchemy + Alembic, JWT 인증, bcrypt 해싱을 사용합니다.

## 요구 사항

- Python 3.9
- PostgreSQL 13+ (로컬: `localhost:5432`)
- OS X / Linux / WSL 권장

## 설치

```bash
python3.9 -m venv .venv
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

`alembic.ini`의 `sqlalchemy.url` 또는 `alembic/env.py`에서 `DATABASE_URL`을 참조하도록 설정하세요.

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

