from typing import Any, Dict, Optional
import os

import requests
from timezonefinder import TimezoneFinder


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

COUNTRY_NAME_TO_CODE = {
    "south korea": "KR",
    "korea": "KR",
    "republic of korea": "KR",
    "united states": "US",
    "usa": "US",
    "japan": "JP",
    "china": "CN",
    "united kingdom": "GB",
    "uk": "GB",
    "france": "FR",
    "germany": "DE",
    "canada": "CA",
    "australia": "AU",
    "netherlands": "NL",
    "india": "IN",
    "united arab emirates": "AE",
    "mexico": "MX",
    "brazil": "BR",
}


def normalize_location_key(city: str, country: str) -> tuple[str, str]:
    return city.strip().lower(), country.strip().lower()


def _split_query(city: str, country: Optional[str]) -> tuple[str, Optional[str]]:
    city = city.strip()
    if country:
        return city, country.strip()

    if "," not in city:
        return city, None

    city_part, country_part = [part.strip() for part in city.split(",", 1)]
    return city_part, country_part or None


def _format_location(city: str, country: str, data: Dict[str, Any], source: str) -> Dict[str, Any]:
    return {
        "city": city.strip(),
        "country": country.strip(),
        "latitude": data["latitude"],
        "longitude": data["longitude"],
        "timezone": data["timezone"],
        "normalized_query": data["normalized_query"],
        "source": source,
    }


def _local_matches(city: str, country: Optional[str], limit: int) -> list[Dict[str, Any]]:
    city_query = city.strip().lower()
    country_query = country.strip().lower() if country else ""
    matches = []

    for (city_key, country_key), local_data in LOCAL_CITY_DATABASE.items():
        if city_query not in city_key and city_query not in local_data["normalized_query"].lower():
            continue

        if country_query and country_query not in country_key:
            continue

        city_name, country_name = local_data["normalized_query"].split(", ", 1)
        matches.append(_format_location(city_name, country_name, local_data, "local_fallback"))

    return matches[:limit]


def _nominatim_matches(city: str, country: Optional[str], limit: int) -> list[Dict[str, Any]]:
    params: dict[str, Any] = {
        "format": "jsonv2",
        "addressdetails": 1,
        "limit": limit,
        "q": f"{city}, {country}" if country else city,
    }

    try:
        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params=params,
            timeout=(3, 7),
            headers={"User-Agent": "savage-fortune-teller/0.1 contact: firebase-hosting"},
        )
        response.raise_for_status()
        payload = response.json()
    except Exception as exc:
        print("DEBUG Nominatim location search failed:", repr(exc))
        return []

    tf = TimezoneFinder()
    matches: list[Dict[str, Any]] = []

    for place in payload:
        try:
            latitude = float(place["lat"])
            longitude = float(place["lon"])
        except (KeyError, TypeError, ValueError):
            continue

        timezone = tf.timezone_at(lng=longitude, lat=latitude)
        if not timezone:
            continue

        address = place.get("address", {})
        city_name = (
            address.get("city")
            or address.get("town")
            or address.get("village")
            or address.get("municipality")
            or place.get("name")
            or city
        )
        country_name = address.get("country") or country or ""
        normalized_query = place.get("display_name") or ", ".join(
            part for part in [city_name, country_name] if part
        )

        matches.append(
            {
                "city": city_name,
                "country": country_name,
                "latitude": latitude,
                "longitude": longitude,
                "timezone": timezone,
                "normalized_query": normalized_query,
                "source": "nominatim",
            }
        )

    return matches


def _geonames_matches(city: str, country: Optional[str], limit: int) -> list[Dict[str, Any]]:
    username = os.getenv("GEONAMES_USERNAME")
    if not username:
        return []

    params: dict[str, Any] = {
        "q": city,
        "maxRows": limit,
        "orderby": "relevance",
        "featureClass": "P",
        "type": "json",
        "username": username,
    }

    if country:
        country_code = COUNTRY_NAME_TO_CODE.get(country.strip().lower())
        if country_code:
            params["country"] = country_code

    try:
        response = requests.get(
            "https://api.geonames.org/searchJSON",
            params=params,
            timeout=(3, 7),
            headers={"User-Agent": "savage-fortune-teller/0.1"},
        )
        response.raise_for_status()
        payload = response.json()
    except Exception as exc:
        print("DEBUG GeoNames location search failed:", repr(exc))
        return []

    if payload.get("status"):
        print("DEBUG GeoNames status:", payload["status"])
        return []

    tf = TimezoneFinder()
    matches: list[Dict[str, Any]] = []

    for place in payload.get("geonames", []):
        try:
            latitude = float(place["lat"])
            longitude = float(place["lng"])
        except (KeyError, TypeError, ValueError):
            continue

        timezone = tf.timezone_at(lng=longitude, lat=latitude)
        if not timezone:
            continue

        display_parts = [
            place.get("name"),
            place.get("adminName1"),
            place.get("countryName"),
        ]
        normalized_query = ", ".join([part for part in display_parts if part])

        matches.append(
            {
                "city": place.get("name") or city,
                "country": place.get("countryName") or country or "",
                "latitude": latitude,
                "longitude": longitude,
                "timezone": timezone,
                "normalized_query": normalized_query,
                "source": "geonames",
            }
        )

    return matches


def _dedupe_locations(locations: list[Dict[str, Any]], limit: int) -> list[Dict[str, Any]]:
    seen: set[tuple[str, str]] = set()
    deduped: list[Dict[str, Any]] = []

    for location in locations:
        key = (
            str(location.get("normalized_query", "")).lower(),
            f"{location.get('latitude')},{location.get('longitude')}",
        )
        if key in seen:
            continue
        seen.add(key)
        deduped.append(location)
        if len(deduped) >= limit:
            break

    return deduped


def search_local_location(city: str, country: str) -> Optional[Dict[str, Any]]:
    city_key, country_key = normalize_location_key(city, country)

    local_data = LOCAL_CITY_DATABASE.get((city_key, country_key))

    if local_data:
        return _format_location(city.strip(), country.strip(), local_data, "local_fallback")

    geonames = _geonames_matches(city, country, 1)
    if geonames:
        return geonames[0]

    nominatim = _nominatim_matches(city, country, 1)
    return nominatim[0] if nominatim else None


def list_matching_locations(
    city: str,
    country: Optional[str] = None,
    limit: int = 8,
) -> list[Dict[str, Any]]:
    city_query, country_query = _split_query(city, country)
    if not city_query:
        return []

    local = _local_matches(city_query, country_query, limit)
    remaining_after_local = max(limit - len(local), 0)
    geonames = _geonames_matches(city_query, country_query, remaining_after_local)
    remaining_after_geonames = max(limit - len(local) - len(geonames), 0)
    nominatim = _nominatim_matches(city_query, country_query, remaining_after_geonames)
    return _dedupe_locations([*local, *geonames, *nominatim], limit)
