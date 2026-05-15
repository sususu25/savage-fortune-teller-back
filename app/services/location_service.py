from typing import Optional, Dict, Any


LOCAL_CITY_DATABASE = {
    ("seoul", "south korea"): {
        "latitude": 37.5665,
        "longitude": 126.9780,
        "timezone": "Asia/Seoul",
        "normalized_query": "Seoul, South Korea",
    },
    ("gunpo", "south korea"): {
        "latitude": 37.3617,
        "longitude": 126.9352,
        "timezone": "Asia/Seoul",
        "normalized_query": "Gunpo, South Korea",
    },
    ("paris", "france"): {
        "latitude": 48.8566,
        "longitude": 2.3522,
        "timezone": "Europe/Paris",
        "normalized_query": "Paris, France",
    },
}


def normalize_location_key(city: str, country: str) -> tuple[str, str]:
    return city.strip().lower(), country.strip().lower()


def search_local_location(city: str, country: str) -> Optional[Dict[str, Any]]:
    city_key, country_key = normalize_location_key(city, country)

    local_data = LOCAL_CITY_DATABASE.get((city_key, country_key))

    if not local_data:
        return None

    return {
        "city": city.strip(),
        "country": country.strip(),
        "latitude": local_data["latitude"],
        "longitude": local_data["longitude"],
        "timezone": local_data["timezone"],
        "normalized_query": local_data["normalized_query"],
        "source": "local_fallback",
    }