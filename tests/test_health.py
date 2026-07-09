from fastapi.testclient import TestClient

from fastapi import FastAPI

from app.api.v1.endpoints.health import router as health_router


api_app = FastAPI()
api_app.include_router(health_router, prefix="/api/v1")
client = TestClient(api_app)


def test_health_check():
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
