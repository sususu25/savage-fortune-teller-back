from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.config import settings


app = FastAPI(title=settings.PROJECT_NAME)

backend_cors_origins = settings.backend_cors_origins
allow_all_origins = "*" in backend_cors_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=backend_cors_origins,
    allow_credentials=not allow_all_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)
