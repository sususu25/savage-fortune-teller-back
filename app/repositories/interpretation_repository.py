import json
from pathlib import Path
from typing import Any, Dict, List

from app.data.archetype_copy import SECTION_TITLES


SEED_FILE_PATH = Path(__file__).resolve().parents[1] / "seed" / "interpretations_seed.json"


def load_interpretation_rows() -> List[Dict[str, Any]]:
    with SEED_FILE_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def find_interpretations(
    type_code: str,
    score: int,
    lang: str = "en",
) -> Dict[str, str]:
    rows = load_interpretation_rows()

    sections = {section_key: "" for section_key in SECTION_TITLES.keys()}

    matched_rows = [
        row for row in rows
        if row["type_code"] == type_code
        and row["lang"] == lang
        and row["score_min"] <= score <= row["score_max"]
    ]

    for section in sections.keys():
        section_rows = [
            row for row in matched_rows
            if row["section"] == section
        ]

        if section_rows:
            section_rows.sort(key=lambda row: row.get("variant_no", 1))
            sections[section] = section_rows[0]["content"]

    return sections
