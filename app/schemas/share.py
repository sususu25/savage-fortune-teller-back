from typing import Any

from pydantic import BaseModel, Field, field_validator


class ShareCreateRequest(BaseModel):
    result_payload: dict[str, Any] = Field(..., min_length=1)
    input: dict[str, Any] | None = None
    source: str | None = None

    @field_validator("source")
    @classmethod
    def normalize_source(cls, value: str | None) -> str | None:
        if value is None:
            return None

        normalized = value.strip()
        return normalized or None


class ShareCreateResponse(BaseModel):
    share_id: str
    share_path: str
    share_url: str | None = None


class ShareResponse(BaseModel):
    share_id: str
    result_payload: dict[str, Any]
    input: dict[str, Any] | None = None
    source: str | None = None
    created_at: str
    view_count: int = 0
