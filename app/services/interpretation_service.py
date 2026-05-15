from typing import Dict

from app.data.interpretations import INTERPRETATIONS


def get_score_band(score: int) -> str:
    if score <= 39:
        return "0_39"
    if score <= 59:
        return "40_59"
    if score <= 79:
        return "60_79"
    return "80_100"


def get_interpretation_sections(
    primary_type_code: str,
    primary_score: int,
) -> Dict[str, str]:
    score_band = get_score_band(primary_score)

    type_interpretations = INTERPRETATIONS.get(primary_type_code, {})
    band_interpretations = type_interpretations.get(score_band, {})

    return {
        "intro": band_interpretations.get("intro", ""),
        "overall": band_interpretations.get("overall", ""),
        "love": band_interpretations.get("love", ""),
        "career": band_interpretations.get("career", ""),
        "health": band_interpretations.get("health", ""),
        "money": band_interpretations.get("money", ""),
    }