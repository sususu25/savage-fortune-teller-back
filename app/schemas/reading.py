from typing import Optional
from pydantic import BaseModel, field_validator


class ReadingRequest(BaseModel):
    birth_date: str
    birth_time: str
    birth_city: str
    birth_country: str

    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timezone: Optional[str] = None

    @field_validator("birth_city")
    @classmethod
    def validate_birth_city(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("birth_city는 비어 있을 수 없습니다.")

        if len(value) < 2:
            raise ValueError("birth_city는 최소 2자 이상이어야 합니다.")

        if len(value) > 100:
            raise ValueError("birth_city는 너무 길 수 없습니다.")

        return value

    @field_validator("birth_country")
    @classmethod
    def validate_birth_country(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("birth_country는 비어 있을 수 없습니다.")

        if len(value) < 2:
            raise ValueError("birth_country는 최소 2자 이상이어야 합니다.")

        if len(value) > 100:
            raise ValueError("birth_country는 너무 길 수 없습니다.")

        return value