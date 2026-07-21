from __future__ import annotations

from typing import Any, Dict, List, Tuple

from app.services.chart_calculator import calculate_chart
from app.services.feature_extractor import extract_features


LOVE_ARCHETYPES: Dict[str, Dict[str, Any]] = {
    "romantic_detective": {
        "label": "The Romantic Detective",
        "viral_alias": "The FBI Agent of Feelings",
        "badge": "investigating chemistry",
        "headline": "You do not fall in love. You open a case file and call it intuition.",
        "weights": {
            "scorpio_emphasis": 14,
            "eighth_house_emphasis": 16,
            "venus_pluto_hard": 18,
            "moon_pluto_hard": 16,
            "relationship_intensity_signature": 18,
            "water_dominance": 8,
            "seventh_house_emphasis": 10,
        },
    },
    "standards_department": {
        "label": "The Standards Department",
        "viral_alias": "The Velvet Rope With Wi-Fi",
        "badge": "selectively available",
        "headline": "Your heart has admissions criteria, mood lighting, and a suspicious guest list.",
        "weights": {
            "venus_angular": 18,
            "libra_emphasis": 14,
            "taurus_emphasis": 12,
            "seventh_house_emphasis": 12,
            "second_house_emphasis": 12,
            "venus_jupiter_easy": 14,
            "mars_venus_strong": 10,
        },
    },
    "chaotic_flirt": {
        "label": "The Chaotic Flirt",
        "viral_alias": "The Romantic Jump Scare",
        "badge": "chemistry hazard",
        "headline": "You bring spark, speed, and the emotional seatbelt nobody can find.",
        "weights": {
            "mars_angular": 16,
            "aries_emphasis": 14,
            "fire_dominance": 12,
            "fifth_house_emphasis": 12,
            "mars_venus_strong": 18,
            "venus_mars_hard": 16,
            "uranus_moon_hard": 8,
        },
    },
    "fantasy_prisoner": {
        "label": "The Fantasy Prisoner",
        "viral_alias": "The Delulu With Great Lighting",
        "badge": "romantic fog machine",
        "headline": "You can turn one ambiguous look into a trilogy with bonus tracks.",
        "weights": {
            "moon_neptune_strong": 18,
            "sun_neptune_strong": 10,
            "asc_neptune_strong": 12,
            "pisces_emphasis": 14,
            "twelfth_house_emphasis": 14,
            "porous_boundary_signature": 16,
            "water_dominance": 10,
        },
    },
    "emotional_weather_system": {
        "label": "The Emotional Weather System",
        "viral_alias": "The Human Push Notification",
        "badge": "feelings broadcasting",
        "headline": "Your love language is emotional climate change with read receipts.",
        "weights": {
            "moon_angular": 18,
            "cancer_emphasis": 14,
            "fourth_house_emphasis": 12,
            "moon_venus_hard": 14,
            "moon_mars_hard": 12,
            "moon_asc_close": 12,
            "water_dominance": 12,
        },
    },
    "commitment_accountant": {
        "label": "The Commitment Accountant",
        "viral_alias": "The Relationship Auditor",
        "badge": "emotionally due diligent",
        "headline": "You want devotion, but first everyone must survive the compliance review.",
        "weights": {
            "saturn_angular": 12,
            "saturn_venus_hard": 18,
            "saturn_moon_hard": 14,
            "capricorn_emphasis": 12,
            "seventh_house_saturn": 16,
            "seventh_house_emphasis": 10,
            "hard_aspect_dominance": 8,
        },
    },
}


FEATURE_RECEIPTS = {
    "venus_pluto_hard": "Venus-Pluto tension gives attraction a basement, a password, and no chill about subtext.",
    "moon_pluto_hard": "Moon-Pluto tension makes feelings deep enough to require a search team.",
    "mars_pluto_hard": "Mars-Pluto tension turns desire into a power tool with questionable supervision.",
    "eighth_house_emphasis": "8th-house emphasis brings intimacy, obsession, secrets, and the urge to investigate vibes for crimes.",
    "scorpio_emphasis": "Scorpio emphasis adds x-ray vision and absolutely no casual setting.",
    "venus_angular": "Angular Venus makes attraction, taste, and desirability part of the first impression.",
    "libra_emphasis": "Libra emphasis wants romance, aesthetics, and a relationship dynamic with decent lighting.",
    "taurus_emphasis": "Taurus emphasis wants loyalty, touch, consistency, and snacks with emotional meaning.",
    "seventh_house_emphasis": "7th-house emphasis makes partnership central, whether or not anyone signed the waiver.",
    "mars_venus_strong": "Mars-Venus contact gives chemistry a megaphone and occasionally bad judgment.",
    "venus_mars_hard": "Venus-Mars tension makes attraction hot, fast, and allergic to moderation.",
    "fifth_house_emphasis": "5th-house emphasis turns crushes, drama, pleasure, and performance into a full theater season.",
    "moon_neptune_strong": "Moon-Neptune contact makes longing poetic, porous, and suspiciously easy to project onto strangers.",
    "pisces_emphasis": "Pisces emphasis can confuse compassion, fantasy, and a playlist with destiny.",
    "twelfth_house_emphasis": "12th-house emphasis keeps desire private, symbolic, and occasionally trapped in the fog machine.",
    "moon_angular": "Angular Moon puts needs and reactions where everyone can see them.",
    "moon_venus_hard": "Moon-Venus tension wants comfort and romance to solve the same problem.",
    "moon_mars_hard": "Moon-Mars tension makes moods arrive with tiny combat boots.",
    "saturn_venus_hard": "Saturn-Venus tension puts love through a background check before allowing softness.",
    "seventh_house_saturn": "Saturn in the 7th house makes commitment serious, delayed, or weirdly contractual.",
    "capricorn_emphasis": "Capricorn emphasis adds standards, caution, and the urge to treat vulnerability like a quarterly review.",
}


def _normalize_name(value: str) -> str:
    return value.strip().lower().replace(" ", "_")


def _get_body(chart: Dict[str, Any], name: str) -> Dict[str, Any] | None:
    name = _normalize_name(name)
    if name in chart.get("planets", {}):
        return chart["planets"][name]
    if name in chart.get("angles", {}):
        return chart["angles"][name]
    return None


def _has_aspect(chart: Dict[str, Any], p1: str, p2: str, aspect_types: set[str], max_orb: float) -> bool:
    p1 = _normalize_name(p1)
    p2 = _normalize_name(p2)
    for aspect in chart.get("aspects", []):
        a1 = _normalize_name(aspect.get("p1", ""))
        a2 = _normalize_name(aspect.get("p2", ""))
        same_pair = (a1 == p1 and a2 == p2) or (a1 == p2 and a2 == p1)
        if same_pair and _normalize_name(aspect.get("type", "")) in aspect_types and float(aspect.get("orb", 999)) <= max_orb:
            return True
    return False


def _love_features(chart: Dict[str, Any]) -> Dict[str, Any]:
    features = extract_features(chart)
    saturn = _get_body(chart, "saturn")

    features["venus_mars_hard"] = _has_aspect(chart, "venus", "mars", {"square", "opposition", "conjunction"}, 6)
    features["saturn_venus_hard"] = _has_aspect(chart, "saturn", "venus", {"square", "opposition", "conjunction"}, 6)
    features["seventh_house_saturn"] = bool(saturn and saturn.get("house") == 7)

    return features


def _score(weights: Dict[str, int], features: Dict[str, Any]) -> Tuple[int, List[str]]:
    total = 0
    matched: List[str] = []

    for feature_name, weight in weights.items():
        value = features.get(feature_name, 0)
        if isinstance(value, bool):
            if value:
                total += weight
                matched.append(feature_name)
        elif isinstance(value, (int, float)) and value > 0:
            total += min(int(value) * 4, weight)
            matched.append(feature_name)

    return min(total, 100), matched


def _build_sections(primary: Dict[str, Any], matched_features: List[str], chart: Dict[str, Any]) -> Dict[str, str]:
    receipts = [FEATURE_RECEIPTS.get(feature, feature.replace("_", " ")) for feature in matched_features[:4]]
    if not receipts:
        receipts = ["Venus, Mars, Moon, and the relationship houses kept their evidence subtle. Suspiciously tasteful."]

    venus = chart["planets"]["venus"]
    mars = chart["planets"]["mars"]
    moon = chart["planets"]["moon"]

    return {
        "romantic_diagnosis": (
            f"You are {primary['viral_alias']}. In love, your chart does not simply want connection; "
            "it wants a genre, a lighting package, and someone to explain why the room suddenly has tension."
        ),
        "the_receipts": " ".join(receipts),
        "venus_mars_moon": (
            f"Venus in {venus['sign']} house {venus.get('house')} shows what you want. "
            f"Mars in {mars['sign']} house {mars.get('house')} shows how you chase it. "
            f"Moon in {moon['sign']} house {moon.get('house')} shows what your nervous system calls love when nobody is looking."
        ),
        "dating_hazard": (
            "Your main hazard is treating a pattern like a prophecy. Chemistry can be useful evidence, "
            "but it is not a court order from the universe."
        ),
        "court_ordered_advice": (
            "Ask for the thing directly. If the answer needs a decoding ring, a group chat, and three lunar transits, "
            "the answer is probably already wearing a little hat that says no."
        ),
    }


def build_love_reading_result(
    birth_date: str,
    birth_time: str,
    birth_city: str,
    latitude: float | None = None,
    longitude: float | None = None,
    timezone: str | None = None,
) -> dict:
    chart = calculate_chart(
        birth_date=birth_date,
        birth_time=birth_time,
        birth_city=birth_city,
        latitude=latitude,
        longitude=longitude,
        timezone=timezone,
    )
    features = _love_features(chart)

    scored = []
    for code, archetype in LOVE_ARCHETYPES.items():
        score, matched = _score(archetype["weights"], features)
        scored.append(
            {
                "code": code,
                "label": archetype["label"],
                "viral_alias": archetype["viral_alias"],
                "result_badge": archetype["badge"],
                "headline": archetype["headline"],
                "score": score,
                "matched_features": matched,
            }
        )

    scored.sort(key=lambda item: item["score"], reverse=True)
    primary = scored[0]

    return {
        "service": "love_life_roast",
        "primary_love_type": primary,
        "section_titles": {
            "romantic_diagnosis": "Romantic Diagnosis",
            "the_receipts": "The Receipts",
            "venus_mars_moon": "Venus, Mars, Moon: The Crime Scene",
            "dating_hazard": "Dating Hazard",
            "court_ordered_advice": "Court-Ordered Advice",
        },
        "sections": _build_sections(primary, primary["matched_features"], chart),
        "all_love_scores": {item["code"]: item for item in scored},
        "features": features,
        "chart": chart,
    }
