from datetime import UTC, datetime
from secrets import token_urlsafe
from typing import Any

from fastapi.encoders import jsonable_encoder

from app.core.config import settings
from app.repositories import share_repository
from app.schemas.share import ShareCreateRequest


class ShareNotFoundError(Exception):
    pass


def _generate_share_id() -> str:
    return token_urlsafe(6).replace("-", "").replace("_", "")[:8]


def _build_share_url(share_path: str) -> str | None:
    if not settings.PUBLIC_APP_URL:
        return None

    return f"{settings.PUBLIC_APP_URL.rstrip('/')}{share_path}"


def create_share(request: ShareCreateRequest) -> dict[str, Any]:
    created_at = datetime.now(UTC).isoformat()

    for _ in range(5):
        share_id = _generate_share_id()
        if share_repository.get_share_document(share_id) is None:
            break
    else:
        share_id = token_urlsafe(12).replace("-", "").replace("_", "")[:16]

    document = jsonable_encoder(
        {
            "share_id": share_id,
            "result_payload": request.result_payload,
            "input": request.input,
            "source": request.source,
            "created_at": created_at,
            "view_count": 0,
        }
    )

    share_repository.create_share_document(share_id, document)

    share_path = f"/r/{share_id}"
    return {
        "share_id": share_id,
        "share_path": share_path,
        "share_url": _build_share_url(share_path),
    }


def get_share(share_id: str) -> dict[str, Any]:
    document = share_repository.get_share_document(share_id)
    if document is None:
        raise ShareNotFoundError

    share_repository.increment_share_view_count(share_id)

    document["share_id"] = share_id
    document["view_count"] = int(document.get("view_count", 0)) + 1
    return document
