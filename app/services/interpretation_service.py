from typing import Dict

from app.repositories.interpretation_repository import find_interpretations


def get_interpretation_sections(
    primary_type_code: str,
    primary_score: int,
    lang: str = "en",
) -> Dict[str, str]:
    return find_interpretations(
        type_code=primary_type_code,
        score=primary_score,
        lang=lang,
    )