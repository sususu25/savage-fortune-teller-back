from fastapi import APIRouter, HTTPException

from app.schemas.reading import ReadingRequest
from app.services.themed_reading_service import build_themed_reading_result

router = APIRouter()


def _create_themed_reading(theme: str, request: ReadingRequest):
    birth_location = f"{request.birth_city}, {request.birth_country}"

    try:
        result = build_themed_reading_result(
            theme=theme,
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
        print(f"DEBUG unexpected {theme} reading error:", repr(e))
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate {theme} astrology reading.",
        )

    return {
        "message": f"{theme.title()} astrology reading generated successfully.",
        "input": {
            "birth_date": request.birth_date,
            "birth_time": request.birth_time,
            "birth_city": request.birth_city,
            "birth_country": request.birth_country,
        },
        **result,
    }


@router.post("/money-readings")
def create_money_reading(request: ReadingRequest):
    return _create_themed_reading("money", request)


@router.post("/career-readings")
def create_career_reading(request: ReadingRequest):
    return _create_themed_reading("career", request)


@router.post("/energy-readings")
def create_energy_reading(request: ReadingRequest):
    return _create_themed_reading("energy", request)
