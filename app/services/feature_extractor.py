from typing import Any, Dict, List


ANGULAR_HOUSES = {1, 4, 7, 10}
HARD_ASPECTS = {"conjunction", "square", "opposition"}
HARD_WITHOUT_CONJUNCTION = {"square", "opposition"}
SOFT_ASPECTS = {"trine", "sextile"}
EASY_ASPECTS = {"conjunction", "trine", "sextile"}
MAJOR_ASPECTS = {"conjunction", "square", "opposition", "trine", "sextile"}


SIGN_ELEMENTS = {
    "aries": "fire",
    "taurus": "earth",
    "gemini": "air",
    "cancer": "water",
    "leo": "fire",
    "virgo": "earth",
    "libra": "air",
    "scorpio": "water",
    "sagittarius": "fire",
    "capricorn": "earth",
    "aquarius": "air",
    "pisces": "water",
}

SIGN_MODALITIES = {
    "aries": "cardinal",
    "taurus": "fixed",
    "gemini": "mutable",
    "cancer": "cardinal",
    "leo": "fixed",
    "virgo": "mutable",
    "libra": "cardinal",
    "scorpio": "fixed",
    "sagittarius": "mutable",
    "capricorn": "cardinal",
    "aquarius": "fixed",
    "pisces": "mutable",
}

# Traditional chart rulers keep the newer six archetypes on the classic planet axis.
SIGN_RULERS = {
    "aries": "mars",
    "taurus": "venus",
    "gemini": "mercury",
    "cancer": "moon",
    "leo": "sun",
    "virgo": "mercury",
    "libra": "venus",
    "scorpio": "mars",
    "sagittarius": "jupiter",
    "capricorn": "saturn",
    "aquarius": "saturn",
    "pisces": "jupiter",
}

WEIGHTED_PLANETS_BY_SIGN_OR_HOUSE = [
    "sun",
    "moon",
    "mercury",
    "venus",
    "mars",
    "jupiter",
    "saturn",
    "uranus",
    "neptune",
    "pluto",
]

PERSONAL_POINTS = ["sun", "moon", "mercury", "venus", "mars", "asc"]


def _normalize_name(value: str) -> str:
    return value.strip().lower().replace(" ", "_")


def _get_body(chart: Dict[str, Any], name: str) -> Dict[str, Any] | None:
    name = _normalize_name(name)

    if name in chart.get("planets", {}):
        return chart["planets"][name]

    if name in chart.get("angles", {}):
        return chart["angles"][name]

    if name in chart.get("points", {}):
        return chart["points"][name]

    return None


def _find_aspect(
    chart: Dict[str, Any],
    p1: str,
    p2: str,
    allowed_aspects: set[str],
    max_orb: float,
) -> Dict[str, Any] | None:
    p1 = _normalize_name(p1)
    p2 = _normalize_name(p2)

    for aspect in chart.get("aspects", []):
        a1 = _normalize_name(aspect.get("p1", ""))
        a2 = _normalize_name(aspect.get("p2", ""))
        aspect_type = _normalize_name(aspect.get("type", ""))
        orb = float(aspect.get("orb", 999))

        same_pair = (a1 == p1 and a2 == p2) or (a1 == p2 and a2 == p1)

        if same_pair and aspect_type in allowed_aspects and orb <= max_orb:
            return aspect

    return None


def _is_angular(chart: Dict[str, Any], body_name: str) -> bool:
    body = _get_body(chart, body_name)
    if not body:
        return False

    house = body.get("house")
    return house in ANGULAR_HOUSES


def _count_sign_emphasis(chart: Dict[str, Any], target_sign: str) -> int:
    target_sign = _normalize_name(target_sign)
    score = 0

    for planet_name in WEIGHTED_PLANETS_BY_SIGN_OR_HOUSE:
        body = _get_body(chart, planet_name)
        if not body:
            continue

        if _normalize_name(body.get("sign", "")) == target_sign:
            score += 1

    asc = _get_body(chart, "asc")
    if asc and _normalize_name(asc.get("sign", "")) == target_sign:
        score += 2

    return score


def _count_house_emphasis(chart: Dict[str, Any], target_house: int) -> int:
    score = 0

    for planet_name in WEIGHTED_PLANETS_BY_SIGN_OR_HOUSE:
        body = _get_body(chart, planet_name)
        if not body:
            continue

        if body.get("house") == target_house:
            score += 1

    return score


def _count_element_dominance(chart: Dict[str, Any], target_element: str) -> int:
    target_element = _normalize_name(target_element)
    score = 0

    for point_name in PERSONAL_POINTS:
        body = _get_body(chart, point_name)
        if not body:
            continue

        sign = _normalize_name(body.get("sign", ""))
        element = SIGN_ELEMENTS.get(sign)

        if element == target_element:
            score += 1

    return score


def _count_modality_dominance(chart: Dict[str, Any], target_modality: str) -> int:
    target_modality = _normalize_name(target_modality)
    score = 0

    for point_name in PERSONAL_POINTS:
        body = _get_body(chart, point_name)
        if not body:
            continue

        sign = _normalize_name(body.get("sign", ""))
        modality = SIGN_MODALITIES.get(sign)

        if modality == target_modality:
            score += 1

    return score


def _count_hard_aspects(chart: Dict[str, Any]) -> int:
    count = 0

    for aspect in chart.get("aspects", []):
        aspect_type = _normalize_name(aspect.get("type", ""))
        if aspect_type in HARD_ASPECTS:
            count += 1

    return count


def _has_strong_aspect(
    chart: Dict[str, Any],
    p1: str,
    p2: str,
    allowed_aspects: set[str],
    max_orb: float,
) -> bool:
    return _find_aspect(chart, p1, p2, allowed_aspects, max_orb) is not None


def _get_asc_ruler(chart: Dict[str, Any]) -> str | None:
    asc = _get_body(chart, "asc")
    if not asc:
        return None

    asc_sign = _normalize_name(asc.get("sign", ""))
    return SIGN_RULERS.get(asc_sign)


def _asc_ruler_has_hard_personal_aspect(chart: Dict[str, Any]) -> bool:
    asc_ruler = _get_asc_ruler(chart)
    if not asc_ruler:
        return False

    for point_name in PERSONAL_POINTS:
        if point_name in {asc_ruler, "asc"}:
            continue

        if _has_strong_aspect(chart, asc_ruler, point_name, HARD_WITHOUT_CONJUNCTION, 6):
            return True

    return False


def extract_features(chart: Dict[str, Any]) -> Dict[str, Any]:
    features = {
        # Saturn / Burdened One
        "saturn_angular": _is_angular(chart, "saturn"),
        "saturn_sun_hard": _has_strong_aspect(chart, "saturn", "sun", HARD_ASPECTS, 6),
        "saturn_moon_hard": _has_strong_aspect(chart, "saturn", "moon", HARD_ASPECTS, 6),
        "saturn_asc_hard": _has_strong_aspect(chart, "saturn", "asc", HARD_ASPECTS, 5),
        "capricorn_emphasis": _count_sign_emphasis(chart, "capricorn"),
        "tenth_house_emphasis": _count_house_emphasis(chart, 10),
        "sixth_house_emphasis": _count_house_emphasis(chart, 6),
        "hard_aspect_dominance": _count_hard_aspects(chart),

        # Uranus / Chaos Magnet
        "uranus_angular": _is_angular(chart, "uranus"),
        "uranus_moon_hard": _has_strong_aspect(chart, "uranus", "moon", HARD_ASPECTS, 6),
        "uranus_mercury_hard": _has_strong_aspect(chart, "uranus", "mercury", HARD_ASPECTS, 6),
        "uranus_asc_hard": _has_strong_aspect(chart, "uranus", "asc", HARD_ASPECTS, 5),
        "mutable_dominance": _count_modality_dominance(chart, "mutable"),
        "eighth_house_emphasis": _count_house_emphasis(chart, 8),

        # Mercury / Overthinker
        "mercury_angular": _is_angular(chart, "mercury"),
        "mercury_sun_close": _has_strong_aspect(chart, "mercury", "sun", {"conjunction"}, 4),
        "mercury_saturn_hard": _has_strong_aspect(chart, "mercury", "saturn", HARD_ASPECTS, 6),
        "mercury_neptune_hard": _has_strong_aspect(chart, "mercury", "neptune", HARD_ASPECTS, 6),
        "gemini_emphasis": _count_sign_emphasis(chart, "gemini"),
        "virgo_emphasis": _count_sign_emphasis(chart, "virgo"),
        "third_house_emphasis": _count_house_emphasis(chart, 3),
        "air_dominance": _count_element_dominance(chart, "air"),

        # Pluto / Dangerous Heart
        "venus_pluto_hard": _has_strong_aspect(chart, "venus", "pluto", HARD_ASPECTS, 5),
        "moon_pluto_hard": _has_strong_aspect(chart, "moon", "pluto", HARD_ASPECTS, 5),
        "mars_pluto_hard": _has_strong_aspect(chart, "mars", "pluto", HARD_ASPECTS, 5),
        "scorpio_emphasis": _count_sign_emphasis(chart, "scorpio"),
        "fifth_house_emphasis": _count_house_emphasis(chart, 5),
        "seventh_house_emphasis": _count_house_emphasis(chart, 7),

        # Neptune / Haunted Dreamer
        "neptune_angular": _is_angular(chart, "neptune"),
        "moon_neptune_strong": _has_strong_aspect(chart, "moon", "neptune", {"conjunction", "square", "opposition", "trine"}, 6),
        "sun_neptune_strong": _has_strong_aspect(chart, "sun", "neptune", {"conjunction", "square", "opposition", "trine"}, 6),
        "asc_neptune_strong": _has_strong_aspect(chart, "neptune", "asc", {"conjunction", "square", "opposition", "trine"}, 5),
        "twelfth_house_emphasis": _count_house_emphasis(chart, 12),
        "pisces_emphasis": _count_sign_emphasis(chart, "pisces"),
        "water_dominance": _count_element_dominance(chart, "water"),

        # Node / Unfinished Legend
        "north_node_sun_strong": _has_strong_aspect(chart, "north_node", "sun", {"conjunction", "trine", "sextile"}, 5),
        "north_node_moon_strong": _has_strong_aspect(chart, "north_node", "moon", {"conjunction", "trine", "sextile"}, 5),
        "north_node_asc_strong": _has_strong_aspect(chart, "north_node", "asc", {"conjunction", "trine", "sextile"}, 5),
        "north_node_mc_strong": _has_strong_aspect(chart, "north_node", "mc", {"conjunction", "trine", "sextile"}, 5),
        "jupiter_mc_strong": _has_strong_aspect(chart, "jupiter", "mc", {"conjunction", "trine", "sextile"}, 5),
        "saturn_node_strong": _has_strong_aspect(chart, "saturn", "north_node", MAJOR_ASPECTS, 5),
        "pluto_node_strong": _has_strong_aspect(chart, "pluto", "north_node", MAJOR_ASPECTS, 5),

        # Classic planet archetypes
        "sun_angular": _is_angular(chart, "sun"),
        "leo_emphasis": _count_sign_emphasis(chart, "leo"),
        "sun_jupiter_easy": _has_strong_aspect(chart, "sun", "jupiter", EASY_ASPECTS, 6),
        "sun_asc_close": _has_strong_aspect(chart, "sun", "asc", {"conjunction"}, 6),
        "fire_dominance": _count_element_dominance(chart, "fire"),
        "moon_angular": _is_angular(chart, "moon"),
        "cancer_emphasis": _count_sign_emphasis(chart, "cancer"),
        "fourth_house_emphasis": _count_house_emphasis(chart, 4),
        "moon_venus_hard": _has_strong_aspect(chart, "moon", "venus", HARD_WITHOUT_CONJUNCTION, 6),
        "moon_mars_hard": _has_strong_aspect(chart, "moon", "mars", HARD_WITHOUT_CONJUNCTION, 6),
        "moon_asc_close": _has_strong_aspect(chart, "moon", "asc", {"conjunction"}, 6),
        "venus_angular": _is_angular(chart, "venus"),
        "libra_emphasis": _count_sign_emphasis(chart, "libra"),
        "taurus_emphasis": _count_sign_emphasis(chart, "taurus"),
        "venus_jupiter_easy": _has_strong_aspect(chart, "venus", "jupiter", EASY_ASPECTS, 6),
        "second_house_emphasis": _count_house_emphasis(chart, 2),
        "first_house_emphasis": _count_house_emphasis(chart, 1),
        "mars_sun_hard": _has_strong_aspect(chart, "mars", "sun", HARD_WITHOUT_CONJUNCTION, 6),
        "mars_saturn_hard": _has_strong_aspect(chart, "mars", "saturn", HARD_WITHOUT_CONJUNCTION, 6),
        "jupiter_angular": _is_angular(chart, "jupiter"),
        "sagittarius_emphasis": _count_sign_emphasis(chart, "sagittarius"),
        "ninth_house_emphasis": _count_house_emphasis(chart, 9),
        "asc_ruler_hard": _asc_ruler_has_hard_personal_aspect(chart),
        "sun_asc_hard": _has_strong_aspect(chart, "sun", "asc", HARD_WITHOUT_CONJUNCTION, 6),
        "asc_moon_hard": _has_strong_aspect(chart, "moon", "asc", HARD_WITHOUT_CONJUNCTION, 6),

        # Secondary-tag helper features
        "mars_angular": _is_angular(chart, "mars"),
        "mars_venus_strong": _has_strong_aspect(chart, "mars", "venus", {"conjunction", "trine", "sextile", "opposition"}, 5),
        "aries_emphasis": _count_sign_emphasis(chart, "aries"),
    }

    features["sudden_change_signature"] = int(
        bool(features["uranus_angular"]) +
        bool(features["uranus_moon_hard"]) +
        bool(features["uranus_mercury_hard"]) +
        (1 if features["mutable_dominance"] >= 3 else 0)
    )

    features["relationship_intensity_signature"] = int(
        bool(features["venus_pluto_hard"]) +
        bool(features["moon_pluto_hard"]) +
        bool(features["mars_pluto_hard"]) +
        (1 if features["seventh_house_emphasis"] >= 2 else 0) +
        (1 if features["eighth_house_emphasis"] >= 2 else 0)
    )

    features["porous_boundary_signature"] = int(
        bool(features["neptune_angular"]) +
        bool(features["moon_neptune_strong"]) +
        (1 if features["twelfth_house_emphasis"] >= 2 else 0) +
        (1 if features["pisces_emphasis"] >= 2 else 0) +
        (1 if features["water_dominance"] >= 3 else 0)
    )

    features["late_bloomer_signature"] = int(
        bool(features["saturn_angular"]) +
        bool(features["north_node_mc_strong"]) +
        bool(features["jupiter_mc_strong"]) +
        bool(features["saturn_node_strong"])
    )

    expansion_score = int(
        bool(features["jupiter_angular"]) +
        bool(features["sun_jupiter_easy"]) +
        bool(features["venus_jupiter_easy"]) +
        (1 if features["sagittarius_emphasis"] >= 2 else 0) +
        (1 if features["ninth_house_emphasis"] >= 2 else 0)
    )
    saturn_moderation = _has_strong_aspect(chart, "jupiter", "saturn", MAJOR_ASPECTS, 6)
    features["jupiter_overextension_signature"] = expansion_score >= 2 and not saturn_moderation

    features["mask_signature"] = (
        features["twelfth_house_emphasis"] >= 3
        and bool(features["asc_ruler_hard"])
    )

    return features
