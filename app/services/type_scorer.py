from typing import Any, Dict

from app.services.chart_calculator import calculate_chart
from app.services.feature_extractor import extract_features
from app.services.archetype_scorer import calculate_full_archetype_result


def calculate_type_scores(
    birth_date: str,
    birth_time: str,
    birth_city: str,
    latitude: float | None = None,
    longitude: float | None = None,
    timezone: str | None = None,
) -> Dict[str, Any]:
    chart = calculate_chart(
        birth_date=birth_date,
        birth_time=birth_time,
        birth_city=birth_city,
        latitude=latitude,
        longitude=longitude,
        timezone=timezone,
    )

    features = extract_features(chart)
    archetype_result = calculate_full_archetype_result(features)

    return {
        "chart": chart,
        "features": features,
        **archetype_result,
    }