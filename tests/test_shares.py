from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.v1.endpoints.shares import router as shares_router
from app.repositories import share_repository


api_app = FastAPI()
api_app.include_router(shares_router, prefix="/api/v1")
client = TestClient(api_app)


def test_create_share_link(monkeypatch):
    stored_documents = {}

    def fake_get_document(share_id):
        return stored_documents.get(share_id)

    def fake_create_document(share_id, data):
        stored_documents[share_id] = data

    monkeypatch.setattr(share_repository, "get_share_document", fake_get_document)
    monkeypatch.setattr(share_repository, "create_share_document", fake_create_document)

    response = client.post(
        "/api/v1/shares",
        json={
            "result_payload": {
                "primary_type": {
                    "code": "overthinker",
                    "score": 76,
                }
            },
            "input": {
                "birth_date": "1995-12-18",
            },
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["share_id"]
    assert body["share_path"] == f"/r/{body['share_id']}"
    assert body["share_url"] is None
    assert stored_documents[body["share_id"]]["view_count"] == 0


def test_get_share_link(monkeypatch):
    def fake_get_document(share_id):
        return {
            "share_id": share_id,
            "result_payload": {
                "primary_type": {
                    "code": "overthinker",
                    "score": 76,
                }
            },
            "input": None,
            "source": None,
            "created_at": "2026-07-10T04:20:00+00:00",
            "view_count": 3,
        }

    monkeypatch.setattr(share_repository, "get_share_document", fake_get_document)
    monkeypatch.setattr(
        share_repository,
        "increment_share_view_count",
        lambda share_id: None,
    )

    response = client.get("/api/v1/shares/abc123")

    assert response.status_code == 200
    assert response.json()["share_id"] == "abc123"
    assert response.json()["view_count"] == 4


def test_get_missing_share_link(monkeypatch):
    monkeypatch.setattr(share_repository, "get_share_document", lambda share_id: None)

    response = client.get("/api/v1/shares/missing")

    assert response.status_code == 404
