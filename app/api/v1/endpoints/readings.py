from fastapi import APIRouter, HTTPException

from app.schemas.reading import ReadingRequest
from app.services.reading_service import build_reading_result

router = APIRouter()


@router.post("/readings")
def create_reading(request: ReadingRequest):
    birth_location = f"{request.birth_city}, {request.birth_country}"

    try:
        result = build_reading_result(
            birth_date=request.birth_date,
            birth_time=request.birth_time,
            birth_city=birth_location,
            latitude=request.latitude,
            longitude=request.longitude,
            timezone=request.timezone,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=str(e),
        )

    except Exception as e:
        print("DEBUG unexpected reading error:", repr(e))
        raise HTTPException(
            status_code=500,
            detail="Failed to generate astrology reading.",
        )

    return {
        "message": "Astrology reading generated successfully.",
        "input": {
            "birth_date": request.birth_date,
            "birth_time": request.birth_time,
            "birth_city": request.birth_city,
            "birth_country": request.birth_country,
        },
        **result,
    }