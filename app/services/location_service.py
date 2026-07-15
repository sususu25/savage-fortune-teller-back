from typing import Any, Dict, Optional


LOCAL_CITY_DATABASE = {
    ("new york", "united states"): {
        "latitude": 40.7128,
        "longitude": -74.0060,
        "timezone": "America/New_York",
        "normalized_query": "New York, United States",
    },
    ("los angeles", "united states"): {
        "latitude": 34.0522,
        "longitude": -118.2437,
        "timezone": "America/Los_Angeles",
        "normalized_query": "Los Angeles, United States",
    },
    ("chicago", "united states"): {
        "latitude": 41.8781,
        "longitude": -87.6298,
        "timezone": "America/Chicago",
        "normalized_query": "Chicago, United States",
    },
    ("london", "united kingdom"): {
        "latitude": 51.5074,
        "longitude": -0.1278,
        "timezone": "Europe/London",
        "normalized_query": "London, United Kingdom",
    },
    ("toronto", "canada"): {
        "latitude": 43.6532,
        "longitude": -79.3832,
        "timezone": "America/Toronto",
        "normalized_query": "Toronto, Canada",
    },
    ("vancouver", "canada"): {
        "latitude": 49.2827,
        "longitude": -123.1207,
        "timezone": "America/Vancouver",
        "normalized_query": "Vancouver, Canada",
    },
    ("sydney", "australia"): {
        "latitude": -33.8688,
        "longitude": 151.2093,
        "timezone": "Australia/Sydney",
        "normalized_query": "Sydney, Australia",
    },
    ("melbourne", "australia"): {
        "latitude": -37.8136,
        "longitude": 144.9631,
        "timezone": "Australia/Melbourne",
        "normalized_query": "Melbourne, Australia",
    },
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
    ("berlin", "germany"): {
        "latitude": 52.5200,
        "longitude": 13.4050,
        "timezone": "Europe/Berlin",
        "normalized_query": "Berlin, Germany",
    },
    ("amsterdam", "netherlands"): {
        "latitude": 52.3676,
        "longitude": 4.9041,
        "timezone": "Europe/Amsterdam",
        "normalized_query": "Amsterdam, Netherlands",
    },
    ("tokyo", "japan"): {
        "latitude": 35.6762,
        "longitude": 139.6503,
        "timezone": "Asia/Tokyo",
        "normalized_query": "Tokyo, Japan",
    },
    ("busan", "south korea"): {
        "latitude": 35.1796,
        "longitude": 129.0756,
        "timezone": "Asia/Seoul",
        "normalized_query": "Busan, South Korea",
    },
    ("singapore", "singapore"): {
        "latitude": 1.3521,
        "longitude": 103.8198,
        "timezone": "Asia/Singapore",
        "normalized_query": "Singapore, Singapore",
    },
    ("hong kong", "hong kong"): {
        "latitude": 22.3193,
        "longitude": 114.1694,
        "timezone": "Asia/Hong_Kong",
        "normalized_query": "Hong Kong, Hong Kong",
    },
    ("mumbai", "india"): {
        "latitude": 19.0760,
        "longitude": 72.8777,
        "timezone": "Asia/Kolkata",
        "normalized_query": "Mumbai, India",
    },
    ("dubai", "united arab emirates"): {
        "latitude": 25.2048,
        "longitude": 55.2708,
        "timezone": "Asia/Dubai",
        "normalized_query": "Dubai, United Arab Emirates",
    },
    ("mexico city", "mexico"): {
        "latitude": 19.4326,
        "longitude": -99.1332,
        "timezone": "America/Mexico_City",
        "normalized_query": "Mexico City, Mexico",
    },
    ("sao paulo", "brazil"): {
        "latitude": -23.5558,
        "longitude": -46.6396,
        "timezone": "America/Sao_Paulo",
        "normalized_query": "Sao Paulo, Brazil",
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


def list_matching_locations(
    city: str,
    country: Optional[str] = None,
    limit: int = 8,
) -> list[Dict[str, Any]]:
    city_query = city.strip().lower()
    country_query = country.strip().lower() if country else ""
    matches = []

    for (city_key, country_key), local_data in LOCAL_CITY_DATABASE.items():
        if city_query not in city_key and city_query not in local_data["normalized_query"].lower():
            continue

        if country_query and country_query not in country_key:
            continue

        city_name, country_name = local_data["normalized_query"].split(", ", 1)
        matches.append(
            {
                "city": city_name,
                "country": country_name,
                "latitude": local_data["latitude"],
                "longitude": local_data["longitude"],
                "timezone": local_data["timezone"],
                "normalized_query": local_data["normalized_query"],
                "source": "local_fallback",
            }
        )

    return matches[:limit]
