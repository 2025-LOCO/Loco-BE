from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # 기본 설정
    PROJECT_NAME: str = "Travel Platform API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "한국 여행 서비스 플랫폼 API"

    # 데이터베이스
    DATABASE_URL: str

    # JWT 설정
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # SGIS API
    SGIS_CONSUMER_KEY: str = ""
    SGIS_CONSUMER_SECRET: str = ""

    # CORS
    ALLOWED_ORIGINS: list[str] = Field(default_factory=lambda: ["http://localhost:5173", "http://localhost:3000"], env="ALLOWED_ORIGINS")

    # Additional settings
    environment: str = Field("production", alias="ENVIRONMENT")
    debug: bool = Field(False, alias="DEBUG")

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )


settings = Settings()