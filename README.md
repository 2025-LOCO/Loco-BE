# 🌏 Travel Platform Backend

> 한국 여행 서비스 플랫폼의 FastAPI 백엔드 서버

현지인 가이드(로코)와 여행자를 연결하는 맞춤형 여행 서비스 플랫폼입니다. 사용자는 지도를 통해 여행지를 선택하고, 현지 가이드와 소통하며, 개인화된 여행 계획을 세울 수 있습니다.

## 📋 목차

- [🎯 프로젝트 개요](#-프로젝트-개요)
- [🛠️ 기술 스택](#️-기술-스택)
- [📁 디렉토리 구조](#-디렉토리-구조)
- [🚀 프로젝트 초기화](#-프로젝트-초기화)
- [🔧 환경 설정](#-환경-설정)
- [📊 데이터베이스 설정](#-데이터베이스-설정)
- [🌐 API 사용법](#-api-사용법)
- [🧪 테스트](#-테스트)
- [📚 추가 리소스](#-추가-리소스)

## 🎯 프로젝트 개요

### 주요 기능

- **🔐 사용자 인증**: JWT 기반 회원가입/로그인 시스템
- **🗺️ 지역 관리**: 통계청 SGIS API 연동으로 실시간 행정구역 정보 제공
- **🧳 맞춤여정**: 사용자별 여행 계획 생성 및 관리
- **👥 로코 시스템**: 현지 가이드 등록 및 매칭 서비스
- **💬 로코톡톡**: 가이드와 여행자 간 실시간 메시징
- **🔍 스마트 검색**: 지역, 평점, 전문분야별 가이드 검색

### 서비스 아키텍처

```
프론트엔드 (React + TypeScript)
           ↕️
백엔드 API (FastAPI + PostgreSQL)
           ↕️
외부 API (통계청 SGIS)
```

## 🛠️ 기술 스택

### 백엔드 프레임워크
- **FastAPI**: 고성능 비동기 웹 프레임워크
- **Python 3.8+**: 메인 프로그래밍 언어
- **Uvicorn**: ASGI 서버

### 데이터베이스 & ORM
- **PostgreSQL**: 관계형 데이터베이스
- **SQLAlchemy**: Python ORM
- **Alembic**: 데이터베이스 마이그레이션 도구

### 인증 & 보안
- **JWT (JSON Web Tokens)**: 토큰 기반 인증
- **BCrypt**: 비밀번호 해싱
- **Python-JOSE**: JWT 처리

### API & 검증
- **Pydantic**: 데이터 검증 및 직렬화
- **HTTPX**: 비동기 HTTP 클라이언트 (SGIS API 연동용)

## 📁 디렉토리 구조

```
backend/
├── app/                           # 메인 애플리케이션 디렉토리
│   ├── __init__.py
│   ├── main.py                    # FastAPI 앱 진입점 (서버 실행 파일)
│   │
│   ├── core/                      # 핵심 설정 및 구성
│   │   ├── __init__.py
│   │   ├── config.py              # 환경변수 및 앱 설정 관리
│   │   ├── security.py            # JWT 토큰, 비밀번호 암호화 로직
│   │   └── database.py            # PostgreSQL 연결 및 세션 관리
│   │
│   ├── api/                       # API 라우터 및 엔드포인트
│   │   ├── __init__.py
│   │   ├── deps.py                # 의존성 주입 (인증, DB 세션 등)
│   │   └── v1/                    # API 버전 1
│   │       ├── __init__.py
│   │       ├── api.py             # 모든 라우터를 통합하는 파일
│   │       └── endpoints/         # 각 도메인별 API 엔드포인트
│   │           ├── __init__.py
│   │           ├── auth.py        # 회원가입, 로그인 API
│   │           ├── users.py       # 사용자 프로필 관리 API
│   │           ├── regions.py     # 지역 정보 조회 API
│   │           ├── trips.py       # 여행 계획 CRUD API
│   │           ├── locos.py       # 로코(가이드) 관리 API
│   │           └── messages.py    # 메시징 시스템 API
│   │
│   ├── models/                    # SQLAlchemy ORM 모델 (데이터베이스 테이블 정의)
│   │   ├── __init__.py
│   │   ├── user.py                # 사용자 테이블 모델
│   │   ├── region.py              # 지역 정보 테이블 모델
│   │   ├── trip.py                # 여행 계획 테이블 모델
│   │   ├── loco.py                # 로코 프로필 테이블 모델
│   │   └── message.py             # 메시지 테이블 모델
│   │
│   ├── schemas/                   # Pydantic 스키마 (API 요청/응답 데이터 검증)
│   │   ├── __init__.py
│   │   ├── user.py                # 사용자 관련 스키마
│   │   ├── region.py              # 지역 정보 스키마
│   │   ├── trip.py                # 여행 계획 스키마
│   │   ├── loco.py                # 로코 프로필 스키마
│   │   └── message.py             # 메시지 스키마
│   │
│   ├── crud/                      # CRUD 작업 (Create, Read, Update, Delete)
│   │   ├── __init__.py
│   │   ├── base.py                # 기본 CRUD 클래스 (공통 기능)
│   │   ├── user.py                # 사용자 CRUD 작업
│   │   ├── region.py              # 지역 CRUD 작업
│   │   ├── trip.py                # 여행 계획 CRUD 작업
│   │   ├── loco.py                # 로코 CRUD 작업
│   │   └── message.py             # 메시지 CRUD 작업
│   │
│   ├── services/                  # 비즈니스 로직 처리
│   │   ├── __init__.py
│   │   ├── auth_service.py        # 인증 관련 비즈니스 로직
│   │   ├── trip_service.py        # 여행 계획 비즈니스 로직
│   │   ├── loco_service.py        # 로코 매칭 비즈니스 로직
│   │   └── sgis_service.py        # 통계청 SGIS API 연동 서비스
│   │
│   └── utils/                     # 유틸리티 함수
│       ├── __init__.py
│       └── helpers.py             # 공통 도우미 함수들
│
├── tests/                         # 테스트 코드
│   ├── __init__.py
│   └── test_main.py               # 기본 API 테스트
│
├── alembic/                       # 데이터베이스 마이그레이션 관리
│   ├── versions/                  # 마이그레이션 파일들
│   ├── env.py                     # Alembic 환경 설정
│   └── alembic.ini                # Alembic 구성 파일
│
├── requirements.txt               # Python 의존성 패키지 목록
├── .env.example                   # 환경변수 예시 파일
├── .gitignore                     # Git 무시 파일 목록
└── README.md                      # 프로젝트 설명서 (현재 파일)
```

### 디렉토리별 상세 설명

#### 🔧 `app/core/`
앱의 핵심 구성 요소들을 관리합니다.
- `config.py`: 데이터베이스 URL, JWT 설정, API 키 등 환경변수 관리
- `security.py`: 비밀번호 암호화, JWT 토큰 생성/검증
- `database.py`: PostgreSQL 연결 설정 및 세션 관리

#### 🌐 `app/api/`
모든 HTTP API 엔드포인트를 정의합니다.
- `deps.py`: 인증 검사, 데이터베이스 세션 등 공통 의존성
- `endpoints/`: 각 기능별로 분리된 API 라우터들

#### 🗄️ `app/models/`
데이터베이스 테이블 구조를 SQLAlchemy로 정의합니다.
- 각 파일은 하나의 데이터베이스 테이블에 대응
- 테이블 간의 관계(외래키, 일대다 등)도 정의

#### 📝 `app/schemas/`
API 요청/응답 데이터의 형식을 검증합니다.
- 클라이언트가 보내는 데이터 검증
- 서버가 응답하는 데이터 형식 정의

#### 💾 `app/crud/`
데이터베이스 기본 조작 함수들을 정의합니다.
- Create(생성), Read(조회), Update(수정), Delete(삭제)
- 복잡한 쿼리 로직도 포함

#### 🧠 `app/services/`
복잡한 비즈니스 로직을 처리합니다.
- 여러 모델을 조합한 복잡한 작업
- 외부 API 연동
- 비즈니스 규칙 검증

## 🚀 프로젝트 초기화

### 1️⃣ 사전 요구사항

#### Python 설치 확인
```bash
python --version  # Python 3.8 이상 필요
```

#### PostgreSQL 설치
- **Windows**: [PostgreSQL 공식 사이트](https://www.postgresql.org/download/windows/)에서 설치
- **macOS**: `brew install postgresql`
- **Ubuntu**: `sudo apt-get install postgresql postgresql-contrib`

### 2️⃣ 프로젝트 클론 및 디렉토리 생성

```bash
# 프로젝트 디렉토리 생성
mkdir travel-platform-backend
cd travel-platform-backend

# 또는 Git 저장소가 있다면 클론
git clone <your-repository-url>
cd travel-platform-backend
```

### 3️⃣ Python 가상환경 설정

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Windows (명령 프롬프트)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate

# 가상환경이 활성화되면 프롬프트 앞에 (venv)가 표시됩니다
```

### 4️⃣ 의존성 패키지 설치

```bash
# 필요한 모든 Python 패키지 설치
pip install -r requirements.txt

# 설치 확인
pip list
```

### 5️⃣ 환경변수 설정

```bash
# 환경변수 파일 복사
cp .env.example .env

# .env 파일을 편집기로 열어서 설정값 입력
# Windows
notepad .env

# macOS
open .env

# Linux
nano .env
```

## 🔧 환경 설정

### `.env` 파일 설정 예시

```env
# 데이터베이스 연결 설정
DATABASE_URL=postgresql://username:password@localhost:5432/travel_db

# JWT 보안 설정
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 통계청 SGIS API 설정 (선택사항)
SGIS_CONSUMER_KEY=your-sgis-consumer-key
SGIS_CONSUMER_SECRET=your-sgis-consumer-secret

# 개발 환경 설정
ENVIRONMENT=development
DEBUG=True

# CORS 설정 (프론트엔드 주소)
ALLOWED_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
```

### 🔑 중요한 설정값들

#### DATABASE_URL
- PostgreSQL 데이터베이스 연결 정보
- 형식: `postgresql://사용자명:비밀번호@호스트:포트/데이터베이스명`
- 예시: `postgresql://postgres:mypassword@localhost:5432/travel_db`

#### SECRET_KEY
- JWT 토큰 서명에 사용되는 비밀키
- 보안상 매우 중요! 랜덤하고 긴 문자열 사용
- 온라인 랜덤 문자열 생성기 사용 권장

#### SGIS_CONSUMER_KEY/SECRET
- 통계청 SGIS API 사용을 위한 인증키
- [SGIS 공식 사이트](https://sgis.kostat.go.kr/)에서 발급
- 지역 정보 기능 사용 시 필요

## 📊 데이터베이스 설정

### 1️⃣ PostgreSQL 데이터베이스 생성

PostgreSQL에 접속하여 프로젝트용 데이터베이스를 생성합니다.

```bash
# PostgreSQL 접속
psql -U postgres

# 데이터베이스 생성
CREATE DATABASE travel_db;

# 사용자 생성 (선택사항)
CREATE USER travel_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE travel_db TO travel_user;

# 접속 종료
\q
```

### 2️⃣ 데이터베이스 마이그레이션

Alembic을 사용하여 데이터베이스 테이블을 생성합니다.

```bash
# 첫 번째 마이그레이션 파일 생성
alembic revision --autogenerate -m "Initial migration"

# 마이그레이션 실행 (테이블 생성)
alembic upgrade head

# 마이그레이션 상태 확인
alembic current
```

### 3️⃣ 서버 실행

```bash
# 개발 서버 시작 (자동 리로드 포함)
uvicorn app.main:app --reload

# 또는 포트 지정
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

서버가 성공적으로 시작되면 다음과 같은 메시지가 표시됩니다:
```
INFO:     Will watch for changes in these directories: ['/path/to/your/project']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using statreload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## 🌐 API 사용법

### API 문서 확인

서버 실행 후 브라우저에서 다음 주소로 접속하여 API 문서를 확인할 수 있습니다:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 주요 API 엔드포인트

#### 🔐 인증 관련
```
POST /api/v1/auth/register    # 회원가입
POST /api/v1/auth/login       # 로그인
```

#### 👤 사용자 관리
```
GET  /api/v1/users/me         # 내 정보 조회
PUT  /api/v1/users/me         # 내 정보 수정
GET  /api/v1/users/{user_id}  # 사용자 정보 조회
```

#### 🗺️ 지역 정보
```
GET  /api/v1/regions/                    # 모든 지역 조회
GET  /api/v1/regions/level/{level}       # 레벨별 지역 조회
GET  /api/v1/regions/parent/{parent_code} # 하위 지역 조회
```

#### 🧳 여행 계획
```
GET  /api/v1/trips/     # 공개 여행 목록
POST /api/v1/trips/     # 여행 계획 생성
GET  /api/v1/trips/my   # 내 여행 목록
```

#### 👥 로코(가이드)
```
GET  /api/v1/locos/                      # 로코 목록
POST /api/v1/locos/                      # 로코 프로필 생성
GET  /api/v1/locos/region/{region_id}    # 지역별 로코 조회
```

### API 사용 예시

#### 회원가입
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "user@example.com",
       "username": "testuser",
       "password": "secretpassword"
     }'
```

#### 로그인 후 토큰 받기
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=user@example.com&password=secretpassword"
```

#### 인증이 필요한 API 호출
```bash
curl -X GET "http://localhost:8000/api/v1/users/me" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🧪 테스트

### 테스트 실행

```bash
# 모든 테스트 실행
pytest

# 상세한 출력과 함께 테스트 실행
pytest -v

# 특정 테스트 파일 실행
pytest tests/test_main.py

# 커버리지와 함께 테스트 실행
pytest --cov=app
```

### 기본 동작 확인

서버가 정상적으로 동작하는지 확인:

```bash
# 헬스 체크
curl http://localhost:8000/health

# 기대 응답: {"status": "healthy"}

# 기본 엔드포인트
curl http://localhost:8000/

# 기대 응답: {"message": "Travel Platform API is running!"}
```

## 🔄 일반적인 개발 워크플로우

### 1. 새 기능 개발 시
```bash
# 1. 모델 수정 (app/models/)
# 2. 스키마 정의 (app/schemas/)
# 3. CRUD 작성 (app/crud/)
# 4. 서비스 로직 작성 (app/services/)
# 5. API 엔드포인트 작성 (app/api/v1/endpoints/)
# 6. 마이그레이션 생성 및 실행
alembic revision --autogenerate -m "Add new feature"
alembic upgrade head
```

### 2. 데이터베이스 스키마 변경 시
```bash
# 모델 수정 후 마이그레이션 생성
alembic revision --autogenerate -m "Update table schema"

# 마이그레이션 검토 후 실행
alembic upgrade head

# 필요시 롤백
alembic downgrade -1
```

## 🚨 문제 해결

### 자주 발생하는 오류들

#### 1. 데이터베이스 연결 오류
```
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) could not connect to server
```
**해결방법:**
- PostgreSQL 서비스가 실행 중인지 확인
- `.env` 파일의 `DATABASE_URL` 확인
- 데이터베이스와 사용자가 올바르게 생성되었는지 확인

#### 2. 모듈을 찾을 수 없다는 오류
```
ModuleNotFoundError: No module named 'app'
```
**해결방법:**
- 가상환경이 활성화되어 있는지 확인
- 프로젝트 루트 디렉토리에서 명령어 실행
- `pip install -r requirements.txt` 재실행

#### 3. 포트가 이미 사용 중이라는 오류
```
OSError: [Errno 48] Address already in use
```
**해결방법:**
```bash
# 다른 포트 사용
uvicorn app.main:app --reload --port 8001

# 또는 기존 프로세스 종료 후 재시작
```

### 디버깅 팁

#### 로그 확인
```python
# app/main.py에 로그 설정 추가
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### 데이터베이스 상태 확인
```bash
# 현재 마이그레이션 상태
alembic current

# 마이그레이션 히스토리
alembic history

# 테이블 존재 확인 (PostgreSQL)
psql -U postgres -d travel_db -c "\dt"
```

## 📚 추가 리소스

### 공식 문서
- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [SQLAlchemy 문서](https://docs.sqlalchemy.org/)
- [Alembic 문서](https://alembic.sqlalchemy.org/)
- [Pydantic 문서](https://pydantic-docs.helpmanual.io/)

### 유용한 도구들
- **데이터베이스 관리**: [pgAdmin](https://www.pgadmin.org/), [DBeaver](https://dbeaver.io/)
- **API 테스트**: [Postman](https://www.postman.com/), [Insomnia](https://insomnia.rest/)
- **코드 에디터**: [VS Code](https://code.visualstudio.com/), [PyCharm](https://www.jetbrains.com/pycharm/)

### 프로덕션 배포 시 고려사항
- 환경변수를 통한 보안 설정
- 데이터베이스 연결 풀 설정
- 로깅 및 모니터링 구성
- Docker 컨테이너화
- CI/CD 파이프라인 구성

---

## 🤝 기여하기

1. 이 저장소를 Fork합니다
2. 새로운 기능 브랜치를 생성합니다 (`git checkout -b feature/AmazingFeature`)
3. 변경사항을 커밋합니다 (`git commit -m 'Add some AmazingFeature'`)
4. 브랜치를 Push합니다 (`git push origin feature/AmazingFeature`)
5. Pull Request를 생성합니다

## 📝 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 문의사항

프로젝트와 관련된 질문이나 제안사항이 있으시면 이슈를 생성해주세요.

---

**즐거운 개발 되세요! 🚀**