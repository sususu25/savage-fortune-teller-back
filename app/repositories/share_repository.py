from functools import lru_cache
from typing import Any

from app.core.config import settings


@lru_cache
def _get_collection():
    from google.cloud import firestore

    client = firestore.Client(database=settings.FIRESTORE_DATABASE)
    return client.collection(settings.FIRESTORE_SHARES_COLLECTION)


def create_share_document(share_id: str, data: dict[str, Any]) -> None:
    _get_collection().document(share_id).set(data)


def get_share_document(share_id: str) -> dict[str, Any] | None:
    snapshot = _get_collection().document(share_id).get()
    if not snapshot.exists:
        return None

    return snapshot.to_dict()


def increment_share_view_count(share_id: str) -> None:
    from google.cloud import firestore

    _get_collection().document(share_id).update(
        {
            "view_count": firestore.Increment(1),
        }
    )
