from fastapi import APIRouter, Query, HTTPException

from app.services.location_service import search_local_location

router = APIRouter()


@router.get("/locations/search")
def search_location(
    city: str = Query(..., min_length=2),
    country: str = Query(..., min_length=2),
):
    location = search_local_location(city=city, country=country)

    if not location:
        raise HTTPException(
            status_code=404,
            detail=f"Location not found in local database: {city}, {country}",
        )

    return {
        "message": "Location found successfully.",
        "location": location,
    }