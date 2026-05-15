from fastapi import APIRouter, Query, HTTPException

from app.services.location_service import search_local_location

router = APIRouter()


@router.get("/locations/search")
def search_location(
    city: str = Query(..., min_length=2),
    country: str = Query(..., min_length=2),
):
    try:
        location = search_local_location(city=city, country=country)

        if not location:
            raise HTTPException(
                status_code=404,
                detail={
                    "message": "Location not found.",
                    "city": city,
                    "country": country,
                    "hint": "This location is not registered in the local location database yet.",
                },
            )

        return {
            "message": "Location found successfully.",
            "location": location,
        }

    except HTTPException:
        raise

    except Exception as e:
        print("DEBUG unexpected location search error:", repr(e))
        raise HTTPException(
            status_code=500,
            detail="Failed to search location.",
        )