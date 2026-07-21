from fastapi import APIRouter

from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.readings import router as readings_router
from app.api.v1.endpoints.love_readings import router as love_readings_router
from app.api.v1.endpoints.locations import router as locations_router
from app.api.v1.endpoints.shares import router as shares_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(readings_router)
api_router.include_router(love_readings_router)
api_router.include_router(locations_router)
api_router.include_router(shares_router)
