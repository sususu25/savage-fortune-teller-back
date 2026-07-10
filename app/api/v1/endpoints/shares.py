from fastapi import APIRouter, HTTPException

from app.schemas.share import ShareCreateRequest, ShareCreateResponse, ShareResponse
from app.services.share_service import ShareNotFoundError, create_share, get_share

router = APIRouter()


@router.post("/shares", response_model=ShareCreateResponse)
def create_share_link(request: ShareCreateRequest):
    try:
        return create_share(request)
    except Exception as e:
        print("DEBUG unexpected share creation error:", repr(e))
        raise HTTPException(
            status_code=500,
            detail="Failed to create share link.",
        )


@router.get("/shares/{share_id}", response_model=ShareResponse)
def get_share_link(share_id: str):
    try:
        return get_share(share_id)
    except ShareNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Share link not found.",
        )
    except Exception as e:
        print("DEBUG unexpected share lookup error:", repr(e))
        raise HTTPException(
            status_code=500,
            detail="Failed to load share link.",
        )
