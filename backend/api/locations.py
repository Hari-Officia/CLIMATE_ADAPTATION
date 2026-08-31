from typing import List
from fastapi import APIRouter, Query, HTTPException
from backend.services.geocoding_service import GeocodingService
from backend.schemas.location import LocationSearchResult, ReverseGeocodeResult

router = APIRouter(tags=["Locations & Geocoding"])

@router.get("/search", response_model=List[LocationSearchResult])
async def search_locations(
    q: str = Query(..., min_length=1, description="Search term for landmark or district"),
    limit: int = Query(8, ge=1, le=20)
):
    geocoding_service = GeocodingService.get_instance()
    results = await geocoding_service.search_locations(query=q, limit=limit)
    return results

@router.get("/reverse", response_model=ReverseGeocodeResult)
async def reverse_geocode(
    lat: float = Query(..., ge=-90.0, le=90.0),
    lon: float = Query(..., ge=-180.0, le=180.0)
):
    geocoding_service = GeocodingService.get_instance()
    result = geocoding_service.reverse_geocode(lat=lat, lon=lon)
    return result
