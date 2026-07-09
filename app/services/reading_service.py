from app.services.type_scorer import calculate_type_scores
from app.services.interpretation_selector import select_interpretations
from app.data.archetype_copy import SECTION_TITLES, get_archetype_copy


def build_reading_result(
    birth_date: str,
    birth_time: str,
    birth_city: str,
    latitude: float | None = None,
    longitude: float | None = None,
    timezone: str | None = None,
) -> dict:
    scoring_result = calculate_type_scores(
        birth_date=birth_date,
        birth_time=birth_time,
        birth_city=birth_city,
        latitude=latitude,
        longitude=longitude,
        timezone=timezone,
    )

    primary = scoring_result["primary_archetype"]
    primary_copy = get_archetype_copy(
        type_code=primary["code"],
        score=primary["score"],
    )

    sections = select_interpretations(
        primary_type_code=primary["code"],
        primary_score=primary["score"],
    )

    return {
        "primary_type": {
            "code": primary["code"],
            "label": primary["label"],
            "score": primary["score"],
            "matched_features": primary["matched_features"],
            **primary_copy,
        },
        "secondary_tags": scoring_result["active_secondary_tags"],
        "section_titles": SECTION_TITLES,
        "sections": sections,
        "all_archetype_scores": scoring_result["archetype_scores"],
        "all_secondary_tag_scores": scoring_result["secondary_tag_scores"],
        "features": scoring_result["features"],
        "chart": scoring_result["chart"],
    }
