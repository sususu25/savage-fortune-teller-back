from __future__ import annotations

import os
import requests
import urllib3
from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Any, Dict, List

from dotenv import load_dotenv
from timezonefinder import TimezoneFinder
import swisseph as swe

load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
        "normalized_query": "Gunpo, Gyeonggi-do, South Korea",
    },
    ("busan", "south korea"): {
        "latitude": 35.1796,
        "longitude": 129.0756,
        "timezone": "Asia/Seoul",
        "normalized_query": "Busan, South Korea",
    },
    ("incheon", "south korea"): {
        "latitude": 37.4563,
        "longitude": 126.7052,
        "timezone": "Asia/Seoul",
        "normalized_query": "Incheon, South Korea",
    },
    ("daegu", "south korea"): {
        "latitude": 35.8714,
        "longitude": 128.6014,
        "timezone": "Asia/Seoul",
        "normalized_query": "Daegu, South Korea",
    },
    ("paris", "france"): {
        "latitude": 48.8566,
        "longitude": 2.3522,
        "timezone": "Europe/Paris",
        "normalized_query": "Paris, France",
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
}

PLANET_MAP = {
    "sun": swe.SUN,
    "moon": swe.MOON,
    "mercury": swe.MERCURY,
    "venus": swe.VENUS,
    "mars": swe.MARS,
    "jupiter": swe.JUPITER,
    "saturn": swe.SATURN,
    "uranus": swe.URANUS,
    "neptune": swe.NEPTUNE,
    "pluto": swe.PLUTO,
    "north_node": swe.MEAN_NODE,
}

ZODIAC_SIGNS = [
    "aries",
    "taurus",
    "gemini",
    "cancer",
    "leo",
    "virgo",
    "libra",
    "scorpio",
    "sagittarius",
    "capricorn",
    "aquarius",
    "pisces",
]

ASPECT_DEGREES = {
    "conjunction": 0,
    "sextile": 60,
    "square": 90,
    "trine": 120,
    "opposition": 180,
}

DEFAULT_ORBS = {
    "sun": 8,
    "moon": 8,
    "mercury": 6,
    "venus": 6,
    "mars": 6,
    "jupiter": 6,
    "saturn": 6,
    "uranus": 5,
    "neptune": 5,
    "pluto": 5,
    "north_node": 5,
    "asc": 5,
    "mc": 5,
}


@dataclass
class GeoResult:
    latitude: float
    longitude: float
    timezone: str
    normalized_query: str
    source: str


def _decimal_hours(hour: int, minute: int) -> float:
    return hour + (minute / 60.0)


def _normalize_longitude(value: float) -> float:
    return value % 360.0


def _longitude_to_sign(longitude: float) -> str:
    normalized = _normalize_longitude(longitude)
    sign_index = int(normalized // 30)
    return ZODIAC_SIGNS[sign_index]


def _longitude_to_degree_in_sign(longitude: float) -> float:
    normalized = _normalize_longitude(longitude)
    return round(normalized % 30, 4)


def _find_house(longitude: float, cusps: List[float]) -> int:
    lon = _normalize_longitude(longitude)
    normalized_cusps = [_normalize_longitude(cusp) for cusp in cusps]

    for i in range(12):
        start = normalized_cusps[i]
        end = normalized_cusps[(i + 1) % 12]
        house_no = i + 1

        if start <= end:
            if start <= lon < end:
                return house_no
        else:
            if lon >= start or lon < end:
                return house_no

    return 12


def _aspect_orb_limit(p1: str, p2: str) -> float:
    return min(DEFAULT_ORBS.get(p1, 5), DEFAULT_ORBS.get(p2, 5))


def _angular_distance(a: float, b: float) -> float:
    diff = abs(_normalize_longitude(a) - _normalize_longitude(b))
    return min(diff, 360 - diff)


def _build_aspects(bodies: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    names = list(bodies.keys())
    aspects: List[Dict[str, Any]] = []

    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            p1 = names[i]
            p2 = names[j]
            lon1 = bodies[p1]["longitude"]
            lon2 = bodies[p2]["longitude"]

            distance = _angular_distance(lon1, lon2)
            orb_limit = _aspect_orb_limit(p1, p2)

            for aspect_name, aspect_degree in ASPECT_DEGREES.items():
                orb = abs(distance - aspect_degree)
                if orb <= orb_limit:
                    aspects.append(
                        {
                            "p1": p1,
                            "p2": p2,
                            "type": aspect_name,
                            "orb": round(orb, 4),
                        }
                    )
                    break

    return aspects


def geocode_birth_city(city_query: str) -> GeoResult:
    username = os.getenv("GEONAMES_USERNAME")

    if not username:
        raise ValueError("GEONAMES_USERNAME is not set in .env")

    normalized_query = city_query.strip()

    if "," in normalized_query:
        city, country = [part.strip() for part in normalized_query.split(",", 1)]
    else:
        city = normalized_query
        country = "South Korea"

    city_key = city.strip().lower()
    country_key = country.strip().lower()

    local_data = LOCAL_CITY_DATABASE.get((city_key, country_key))
    country_code = COUNTRY_NAME_TO_CODE.get(country_key)

    params = {
        "q": city,
        "maxRows": 1,
        "orderby": "relevance",
        "featureClass": "P",
        "type": "json",
        "username": username,
    }

    if country_code:
        params["country"] = country_code

    # 1) GeoNames 먼저 시도
    try:
        print("DEBUG trying GeoNames:", params)

        response = requests.get(
            "https://api.geonames.org/searchJSON",
            params=params,
            timeout=(3, 7),
            headers={
                "User-Agent": "savage-fortune-teller/0.1"
            },
        )

        response.raise_for_status()
        data = response.json()

        status = data.get("status")
        if status:
            message = status.get("message", "GeoNames API error")
            raise ValueError(f"GeoNames API error: {message}")

        results = data.get("geonames", [])
        if not results:
            raise ValueError(f"Could not find city from GeoNames: {city_query}")

        place = results[0]

        latitude = float(place["lat"])
        longitude = float(place["lng"])

        tf = TimezoneFinder()
        timezone_name = tf.timezone_at(lng=longitude, lat=latitude)

        if not timezone_name:
            raise ValueError("Could not determine timezone from coordinates.")

        display_parts = [
            place.get("name"),
            place.get("adminName1"),
            place.get("countryName"),
        ]
        normalized_location = ", ".join([part for part in display_parts if part])

        print("DEBUG GeoNames matched:", normalized_location)

        return GeoResult(
            latitude=latitude,
            longitude=longitude,
            timezone=timezone_name,
            normalized_query=normalized_location,
            source="geonames",
        )

    except Exception as e:
        print("DEBUG GeoNames failed:", repr(e))

    # 2) GeoNames 실패 시 local fallback
    if local_data:
        print("DEBUG local fallback matched:", local_data["normalized_query"])

        return GeoResult(
            latitude=local_data["latitude"],
            longitude=local_data["longitude"],
            timezone=local_data["timezone"],
            normalized_query=local_data["normalized_query"],
            source="local_fallback",
        )

    raise ValueError(
        f"Could not geocode location. GeoNames failed and no local fallback found for key: {(city_key, country_key)}"
    )


def calculate_chart(
    birth_date: str,
    birth_time: str,
    birth_city: str,
    latitude: float | None = None,
    longitude: float | None = None,
    timezone: str | None = None,
) -> Dict[str, Any]:
    year, month, day = map(int, birth_date.split("-"))
    hour, minute = map(int, birth_time.split(":"))

    if latitude is not None and longitude is not None and timezone is not None:
        geo = GeoResult(
            latitude=latitude,
            longitude=longitude,
            timezone=timezone,
            normalized_query=birth_city,
            source="request_location",
        )
    else:
        geo = geocode_birth_city(birth_city)


    local_dt = datetime(year, month, day, hour, minute, tzinfo=ZoneInfo(geo.timezone))
    utc_dt = local_dt.astimezone(ZoneInfo("UTC"))

    jd_ut = swe.julday(
        utc_dt.year,
        utc_dt.month,
        utc_dt.day,
        _decimal_hours(utc_dt.hour, utc_dt.minute),
        swe.GREG_CAL,
    )

    flags = swe.FLG_SWIEPH | swe.FLG_SPEED

    planet_positions: Dict[str, Dict[str, Any]] = {}

    # 하우스 계산
    house_result = swe.houses(jd_ut, geo.latitude, geo.longitude, b"P")
    cusps = list(house_result[0])[:12]
    ascmc = list(house_result[1])

    asc_longitude = ascmc[0]
    mc_longitude = ascmc[1]

    # 행성/노드 계산
    for body_name, body_code in PLANET_MAP.items():
        calc_result = swe.calc_ut(jd_ut, body_code, flags)
        values = calc_result[0]
        longitude = values[0]

        planet_positions[body_name] = {
            "sign": _longitude_to_sign(longitude),
            "house": _find_house(longitude, cusps),
            "degree": _longitude_to_degree_in_sign(longitude),
            "longitude": round(_normalize_longitude(longitude), 6),
        }

    angle_positions = {
        "asc": {
            "sign": _longitude_to_sign(asc_longitude),
            "degree": _longitude_to_degree_in_sign(asc_longitude),
            "longitude": round(_normalize_longitude(asc_longitude), 6),
        },
        "mc": {
            "sign": _longitude_to_sign(mc_longitude),
            "degree": _longitude_to_degree_in_sign(mc_longitude),
            "longitude": round(_normalize_longitude(mc_longitude), 6),
        },
    }

    bodies_for_aspects = {
        **{
            key: {"longitude": value["longitude"]}
            for key, value in planet_positions.items()
        },
        "asc": {"longitude": angle_positions["asc"]["longitude"]},
        "mc": {"longitude": angle_positions["mc"]["longitude"]},
    }

    aspects = _build_aspects(bodies_for_aspects)

    return {
        "meta": {
            "birth_city_input": birth_city,
            "resolved_location": geo.normalized_query,
            "geocoding_source": geo.source,
            "latitude": round(geo.latitude, 6),
            "longitude": round(geo.longitude, 6),
            "timezone": geo.timezone,
            "local_datetime": local_dt.isoformat(),
            "utc_datetime": utc_dt.isoformat(),
            "julian_day_ut": round(jd_ut, 6),
        },
        "planets": {
            key: {
                "sign": value["sign"],
                "house": value["house"],
                "degree": value["degree"],
                "longitude": value["longitude"],
            }
            for key, value in planet_positions.items()
            if key != "north_node"
        },
        "angles": angle_positions,
        "points": {
            "north_node": {
                "sign": planet_positions["north_node"]["sign"],
                "house": planet_positions["north_node"]["house"],
                "degree": planet_positions["north_node"]["degree"],
                "longitude": planet_positions["north_node"]["longitude"],
            }
        },
        "houses": {
            str(index + 1): round(cusp, 6)
            for index, cusp in enumerate(cusps)
        },
        "aspects": aspects,
    }