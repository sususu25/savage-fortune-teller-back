from typing import Dict

from app.services.interpretation_service import get_interpretation_sections


def select_interpretations(
    primary_type_code: str,
    primary_score: int,
) -> Dict[str, str]:
    return get_interpretation_sections(
        primary_type_code=primary_type_code,
        primary_score=primary_score,
        lang="en",
    )