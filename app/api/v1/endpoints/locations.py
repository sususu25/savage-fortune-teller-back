from fastapi import APIRouter, Query, HTTPException

from app.services.location_service import list_matching_locations, search_local_location

router = APIRouter()


@router.get("/locations/search")
def search_location(
    city: str = Query(..., min_length=2),
    country: str | None = Query(default=None, min_length=2),
    limit: int = Query(default=8, ge=1, le=12),
):
    try:
        locations = list_matching_locations(city=city, country=country, limit=limit)

        if not country:
            return {
                "message": "Location suggestions found successfully.",
                "locations": locations,
            }

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
            "locations": locations,
        }

    except HTTPException:
        raise

    except Exception as e:
        print("DEBUG unexpected location search error:", repr(e))
        raise HTTPException(
            status_code=500,
            detail="Failed to search location.",
        )
