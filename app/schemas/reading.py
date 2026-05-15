from typing import Optional
from datetime import datetime

from pydantic import BaseModel, field_validator


class ReadingRequest(BaseModel):
    birth_date: str
    birth_time: str
    birth_city: str
    birth_country: str

    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timezone: Optional[str] = None

    @field_validator("birth_date")
    @classmethod
    def validate_birth_date(cls, value: str) -> str:
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("birth_date must be in YYYY-MM-DD format.")
        return value

    @field_validator("birth_time")
    @classmethod
    def validate_birth_time(cls, value: str) -> str:
        try:
            datetime.strptime(value, "%H:%M")
        except ValueError:
            raise ValueError("birth_time must be in HH:MM format.")
        return value

    @field_validator("birth_city", "birth_country")
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("birth_city and birth_country cannot be empty.")
        return value.strip()

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, value: Optional[float]) -> Optional[float]:
        if value is not None and not (-90 <= value <= 90):
            raise ValueError("latitude must be between -90 and 90.")
        return value

    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, value: Optional[float]) -> Optional[float]:
        if value is not None and not (-180 <= value <= 180):
            raise ValueError("longitude must be between -180 and 180.")
        return value