from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, field_validator, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    driver: str = "aiosqlite"
    path: str = "."
    name: str = "tasks.db"
    url: str | None = None
    echo: bool = False

    @computed_field
    @property
    def connection_url(self) -> str:
        if self.url:
            return self.url

        db_path = Path(self.path) / self.name
        db_path_str = db_path.as_posix()
        if not db_path_str.startswith("/"):
            db_path_str = f"./{db_path_str}"

        return f"sqlite+{self.driver}:///{db_path_str}"


class SecuritySettings(BaseModel):
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, value: str) -> str:
        if len(value) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        if value == "your-secret-key-change-in-production":
            raise ValueError(
                "SECRET_KEY must be changed from default value in production"
            )
        return value


class AppSettings(BaseModel):
    name: str = "Task Tracker"
    debug: bool = False
    environment: Literal["development", "production", "testing"] = "development"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
        case_sensitive=False,
    )

    app: AppSettings = Field(default_factory=AppSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    security: SecuritySettings

    @field_validator("security", mode="before")
    @classmethod
    def ensure_security_config(cls, v):
        if v is None:
            raise ValueError(
                "Security settings are required. Set SECURITY__SECRET_KEY environment variable."
            )
        return v


settings = Settings()
