import pytest
from backend.services.geocoding_service import GeocodingService

geo = GeocodingService.get_instance()

def test_marina_beach_point_in_polygon():
    # Marina Beach coordinates: (13.05, 80.28)
    res = geo.find_district_by_coordinates(13.0500, 80.2824)
    assert res is not None
    assert res["district_name"] == "Chennai"
    assert res["district_id"] == "chennai"

def test_coimbatore_point_in_polygon():
    res = geo.find_district_by_coordinates(11.0168, 76.9680)
    assert res is not None
    assert res["district_name"] == "Coimbatore"

def test_avadi_point_in_polygon():
    # Avadi: (13.1147, 80.1018) -> Tiruvallur
    res = geo.find_district_by_coordinates(13.1147, 80.1018)
    assert res is not None
    assert res["district_name"] == "Tiruvallur"

def test_outside_tamil_nadu_boundary():
    # Bengaluru (12.9716, 77.5946) or Delhi (28.61, 77.20)
    res = geo.find_district_by_coordinates(28.6139, 77.2090)
    assert res is None

def test_reverse_geocoding():
    rev = geo.reverse_geocode(13.0827, 80.2707)
    assert rev["is_inside_tamil_nadu"] is True
    assert rev["district_name"] == "Chennai"

    rev_outside = geo.reverse_geocode(19.0760, 72.8777) # Mumbai
    assert rev_outside["is_inside_tamil_nadu"] is False
