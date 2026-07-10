import json
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    PROJECT_NAME: str = "Savage Fortune Teller API"
    API_V1_PREFIX: str = "/api/v1"
    BACKEND_CORS_ORIGINS: str = "*"
    GEONAMES_USERNAME: str | None = None
    FIRESTORE_DATABASE: str = "sft-db"
    FIRESTORE_SHARES_COLLECTION: str = "shares"
    PUBLIC_APP_URL: str | None = None

    @property
    def backend_cors_origins(self) -> list[str]:
        value = self.BACKEND_CORS_ORIGINS.strip()
        if not value:
            return []

        if value.startswith("["):
            parsed = json.loads(value)
            if isinstance(parsed, list):
                return [str(origin).strip() for origin in parsed if str(origin).strip()]

        return [origin.strip() for origin in value.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
