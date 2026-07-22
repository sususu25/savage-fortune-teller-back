from typing import Any, Dict, List, Tuple

from app.services.chart_calculator import calculate_chart
from app.services.feature_extractor import (
    SIGN_ELEMENTS,
    SIGN_MODALITIES,
    SIGN_RULERS,
    extract_features,
)


PLANETS = [
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

OUTER_PLANETS = {"uranus", "neptune", "pluto"}
ANGULAR_HOUSES = {1, 4, 7, 10}
PERSONAL_POINTS = {"sun", "moon", "mercury", "venus", "mars", "asc"}
CORE_POINTS = {"sun", "moon", "asc"}
MAJOR_ASPECTS = {"conjunction", "square", "opposition", "trine", "sextile"}
HARD_ASPECTS = {"conjunction", "square", "opposition"}
ORDINAL_HOUSES = {
    1: "1st",
    2: "2nd",
    3: "3rd",
    4: "4th",
    5: "5th",
    6: "6th",
    7: "7th",
    8: "8th",
    9: "9th",
    10: "10th",
    11: "11th",
    12: "12th",
}

PLANET_COPY = {
    "sun": {
        "label": "Solar Type",
        "viral_alias": "The Spotlight With A Birth Certificate",
        "badge": "identity department loud",
        "headline": "Your chart does not enter rooms. It requests lighting.",
        "advice": "Create the thing before demanding applause for the trailer.",
    },
    "moon": {
        "label": "Lunar Type",
        "viral_alias": "The Emotional Weather System",
        "badge": "feelings have admin access",
        "headline": "Your nervous system is the main tenant and everyone else is subletting.",
        "advice": "Name the feeling before it hires a decorator and moves in permanently.",
    },
    "mercury": {
        "label": "Mercurial Type",
        "viral_alias": "The Group Chat Attorney",
        "badge": "brain doing billable hours",
        "headline": "Your thoughts have tabs, footnotes, and an unpaid internship program.",
        "advice": "Ask one direct question before building a courtroom inside your skull.",
    },
    "venus": {
        "label": "Venusian Type",
        "viral_alias": "The Luxury Attachment Problem",
        "badge": "taste with consequences",
        "headline": "Your chart wants beauty, loyalty, pleasure, and a receipt drawer with mood lighting.",
        "advice": "Wanting nice things is allowed. Letting desire drive without insurance is the issue.",
    },
    "mars": {
        "label": "Martian Type",
        "viral_alias": "The Fight Scene In A Cute Outfit",
        "badge": "impulse with a weaponized calendar",
        "headline": "Your drive arrives first and asks the frontal lobe to catch up later.",
        "advice": "Act, yes. But stop mistaking every delay for a personal insult from the cosmos.",
    },
    "jupiter": {
        "label": "Jovian Type",
        "viral_alias": "The Inspirational Overdraft",
        "badge": "faith with expansion damage",
        "headline": "Your chart believes bigger is better and sometimes forgets physics has terms.",
        "advice": "Keep the vision. Add a boundary, a budget, and one boring checkpoint.",
    },
    "saturn": {
        "label": "Saturnian Type",
        "viral_alias": "The Unpaid Adult In The Room",
        "badge": "discipline with back pain",
        "headline": "Your chart brought structure, delay, standards, and a clipboard nobody asked for.",
        "advice": "Responsibility is useful. Turning your spine into public infrastructure is not.",
    },
    "uranus": {
        "label": "Uranian Type",
        "viral_alias": "The Plot Twist With Wi-Fi",
        "badge": "disruption has entered the chat",
        "headline": "Your chart is allergic to scripts, locked doors, and boring explanations.",
        "advice": "Change the system, sure. Stop detonating stability just to prove you have a pulse.",
    },
    "neptune": {
        "label": "Neptunian Type",
        "viral_alias": "The Fog Machine With Prophetic Timing",
        "badge": "intuition without a fence",
        "headline": "Your chart can read a room and then accidentally become the room.",
        "advice": "Intuition is data. Fantasy is seasoning. Do not serve seasoning as dinner.",
    },
    "pluto": {
        "label": "Plutonian Type",
        "viral_alias": "The Emotional X-Ray With Trust Issues",
        "badge": "depth with a search warrant",
        "headline": "Your chart does not skim the surface. It files subpoenas against it.",
        "advice": "Transformation is holy. Surveillance disguised as intimacy is still surveillance.",
    },
}

NATURAL_HOUSES = {
    "sun": {5},
    "moon": {4},
    "mercury": {3, 6},
    "venus": {2, 7},
    "mars": {1, 8},
    "jupiter": {9},
    "saturn": {10},
    "uranus": {11},
    "neptune": {12},
    "pluto": {8},
}

FEATURE_WEIGHTS = {
    "sun": {
        "sun_angular": 18,
        "leo_emphasis": 10,
        "sun_jupiter_easy": 8,
        "sun_asc_close": 18,
        "fire_dominance": 8,
        "fifth_house_emphasis": 8,
    },
    "moon": {
        "moon_angular": 18,
        "cancer_emphasis": 10,
        "fourth_house_emphasis": 12,
        "moon_asc_close": 18,
        "water_dominance": 8,
    },
    "mercury": {
        "mercury_angular": 18,
        "mercury_sun_close": 14,
        "mercury_saturn_hard": 8,
        "mercury_neptune_hard": 8,
        "gemini_emphasis": 8,
        "virgo_emphasis": 8,
        "third_house_emphasis": 12,
        "air_dominance": 8,
    },
    "venus": {
        "venus_angular": 18,
        "libra_emphasis": 8,
        "taurus_emphasis": 8,
        "venus_jupiter_easy": 8,
        "second_house_emphasis": 12,
        "seventh_house_emphasis": 10,
    },
    "mars": {
        "mars_angular": 18,
        "aries_emphasis": 10,
        "first_house_emphasis": 10,
        "eighth_house_emphasis": 8,
        "mars_sun_hard": 8,
        "mars_saturn_hard": 8,
    },
    "jupiter": {
        "jupiter_angular": 18,
        "sagittarius_emphasis": 10,
        "ninth_house_emphasis": 14,
        "jupiter_mc_strong": 18,
        "sun_jupiter_easy": 8,
        "venus_jupiter_easy": 8,
    },
    "saturn": {
        "saturn_angular": 20,
        "capricorn_emphasis": 10,
        "tenth_house_emphasis": 14,
        "sixth_house_emphasis": 8,
        "saturn_sun_hard": 14,
        "saturn_moon_hard": 14,
        "saturn_asc_hard": 16,
        "hard_aspect_dominance": 8,
    },
    "uranus": {
        "uranus_angular": 24,
        "uranus_moon_hard": 18,
        "uranus_mercury_hard": 16,
        "uranus_asc_hard": 22,
        "sudden_change_signature": 12,
    },
    "neptune": {
        "neptune_angular": 24,
        "moon_neptune_strong": 20,
        "sun_neptune_strong": 18,
        "asc_neptune_strong": 22,
        "twelfth_house_emphasis": 12,
        "porous_boundary_signature": 12,
        "water_dominance": 6,
    },
    "pluto": {
        "venus_pluto_hard": 18,
        "moon_pluto_hard": 20,
        "mars_pluto_hard": 18,
        "pluto_node_strong": 12,
        "eighth_house_emphasis": 14,
        "relationship_intensity_signature": 12,
    },
}

FEATURE_RECEIPTS = {
    "angular_house": "{planet} in an angular house makes it hard to hide. The chart put it near a microphone.",
    "angle_aspect": "{planet} has a close contact with a major chart angle, so it acts personal instead of politely staying in the background.",
    "core_point_aspect": "{planet} aspects the Sun, Moon, or Ascendant. That is identity-level evidence, not wallpaper.",
    "personal_aspect_stack": "{planet} has multiple major aspects to personal planets. The chart keeps repeating the same witness.",
    "chart_ruler": "{planet} rules the Ascendant sign, so it manages the front desk of the personality.",
    "natural_house": "{planet} lands in a house where its themes get extra stage time.",
    "house_theme": "{planet}'s house themes repeat across the chart, which is how astrology says 'this again?'",
}

VENUS_REAL_LIFE = (
    "You rarely want something merely because it is useful. It must also feel right, look right, and fit the private movie playing in your head.\n\n"
    "In love, you may crave loyalty and stability while repeatedly being fascinated by people who arrive with unusual circumstances, mixed signals, or an impressive collection of emotional complications.\n\n"
    "With money, you can be disciplined for weeks and then decide that one beautifully designed object is not a purchase but a necessary correction to your quality of life."
)

VENUS_GIFT = (
    "You understand value. You notice quality, atmosphere, presentation, and emotional nuance that other people miss. "
    "When your standards are grounded in reality, your taste becomes discernment rather than decoration."
)

VENUS_DAMAGE = (
    "The problem begins when beauty becomes proof of worth, longing becomes proof of love, "
    "and an expensive preference is promoted to a basic human need."
)

VENUS_VERDICT = (
    "Keep the standards. Check the fantasy. And for heaven's sake, stop calling every emotionally confusing person \"interesting.\""
)


def _title(value: str) -> str:
    return value.replace("_", " ").title()


def _format_planet(value: str) -> str:
    return _title(value)


def _format_degree_minutes(value: float) -> str:
    degree = int(value)
    minutes = int(round((value - degree) * 60))
    if minutes == 60:
        degree += 1
        minutes = 0
    return f"{degree}°{minutes:02d}′"


def _format_house(value: int | None) -> str:
    if not value:
        return "House unknown"
    return f"{ORDINAL_HOUSES.get(value, str(value) + 'th')} House"


def _format_placement(body: Dict[str, Any] | None) -> str:
    if not body:
        return "Unknown"
    house = body.get("house")
    degree = _format_degree_minutes(float(body.get("degree", 0)))
    house_text = f" · {_format_house(int(house))}" if house else ""
    return f"{_title(str(body.get('sign', 'unknown')))} {degree}{house_text}"


def _get_body(chart: Dict[str, Any], name: str) -> Dict[str, Any] | None:
    if name in chart.get("planets", {}):
        return chart["planets"][name]
    if name in chart.get("angles", {}):
        return chart["angles"][name]
    if name in chart.get("points", {}):
        return chart["points"][name]
    return None


def _aspect_matches(aspect: Dict[str, Any], p1: str, p2: str, allowed: set[str], max_orb: float) -> bool:
    a1 = str(aspect.get("p1", "")).lower()
    a2 = str(aspect.get("p2", "")).lower()
    same_pair = (a1 == p1 and a2 == p2) or (a1 == p2 and a2 == p1)
    return same_pair and str(aspect.get("type", "")).lower() in allowed and float(aspect.get("orb", 999)) <= max_orb


def _find_aspects(chart: Dict[str, Any], planet: str, targets: set[str], allowed: set[str], max_orb: float) -> List[Dict[str, Any]]:
    matches = []
    for aspect in chart.get("aspects", []):
        p1 = str(aspect.get("p1", "")).lower()
        p2 = str(aspect.get("p2", "")).lower()
        other = p2 if p1 == planet else p1 if p2 == planet else None
        if other in targets and str(aspect.get("type", "")).lower() in allowed and float(aspect.get("orb", 999)) <= max_orb:
            matches.append(aspect)
    return sorted(matches, key=lambda item: float(item.get("orb", 999)))


def _aspect_label(aspect: Dict[str, Any]) -> str:
    return f"{_format_planet(str(aspect.get('p1', 'unknown')))}-{_format_planet(str(aspect.get('p2', 'unknown')))}"


def _house_count(chart: Dict[str, Any], house: int) -> int:
    count = 0
    for body in chart.get("planets", {}).values():
        if body.get("house") == house:
            count += 1
    return count


def _get_chart_ruler(chart: Dict[str, Any]) -> str | None:
    asc = _get_body(chart, "asc")
    if not asc:
        return None
    return SIGN_RULERS.get(str(asc.get("sign", "")).lower())


def _feature_score(planet: str, features: Dict[str, Any]) -> Tuple[int, List[str]]:
    total = 0
    matched = []
    for feature, weight in FEATURE_WEIGHTS[planet].items():
        value = features.get(feature, 0)
        if isinstance(value, bool):
            if value:
                total += weight
                matched.append(feature)
        elif isinstance(value, (int, float)) and value > 0:
            total += min(int(value) * 4, weight)
            matched.append(feature)
    return total, matched


def _score_planet(planet: str, chart: Dict[str, Any], features: Dict[str, Any], chart_ruler: str | None) -> Dict[str, Any]:
    body = _get_body(chart, planet)
    copy = PLANET_COPY[planet]
    total = 8
    matched_features: List[str] = []
    receipts: List[str] = []

    feature_total, feature_matches = _feature_score(planet, features)
    total += feature_total
    matched_features.extend(feature_matches)

    if chart_ruler == planet:
        total += 24
        matched_features.append("chart_ruler")
        receipts.append(FEATURE_RECEIPTS["chart_ruler"].format(planet=_format_planet(planet)))

    if body and body.get("house") in ANGULAR_HOUSES:
        total += 22 if planet in OUTER_PLANETS else 16
        matched_features.append("angular_house")
        receipts.append(FEATURE_RECEIPTS["angular_house"].format(planet=_format_planet(planet)))

    angle_aspects = _find_aspects(chart, planet, {"asc", "mc"}, MAJOR_ASPECTS, 5)
    if angle_aspects:
        strongest = angle_aspects[0]
        total += 24 if planet in OUTER_PLANETS else 16
        if str(strongest.get("type", "")).lower() == "conjunction":
            total += 6
        matched_features.append("angle_aspect")
        receipts.append(FEATURE_RECEIPTS["angle_aspect"].format(planet=_format_planet(planet)))

    core_targets = CORE_POINTS - {planet}
    core_aspects = _find_aspects(chart, planet, core_targets, MAJOR_ASPECTS, 6)
    if core_aspects:
        total += min(len(core_aspects) * (16 if planet in OUTER_PLANETS else 10), 28)
        matched_features.append("core_point_aspect")
        receipts.append(FEATURE_RECEIPTS["core_point_aspect"].format(planet=_format_planet(planet)))

    personal_targets = PERSONAL_POINTS - {planet}
    personal_aspects = _find_aspects(chart, planet, personal_targets, MAJOR_ASPECTS, 6)
    if len(personal_aspects) >= 2:
        total += min(len(personal_aspects) * (8 if planet in OUTER_PLANETS else 5), 24)
        matched_features.append("personal_aspect_stack")
        receipts.append(FEATURE_RECEIPTS["personal_aspect_stack"].format(planet=_format_planet(planet)))

    if body and body.get("house") in NATURAL_HOUSES[planet]:
        total += 10
        matched_features.append("natural_house")
        receipts.append(FEATURE_RECEIPTS["natural_house"].format(planet=_format_planet(planet)))

    natural_house_count = sum(_house_count(chart, house) for house in NATURAL_HOUSES[planet])
    if natural_house_count >= 2:
        total += min(natural_house_count * 4, 14)
        matched_features.append("house_theme")
        receipts.append(FEATURE_RECEIPTS["house_theme"].format(planet=_format_planet(planet)))

    if planet not in OUTER_PLANETS and body:
        ruled_signs = {sign for sign, ruler in SIGN_RULERS.items() if ruler == planet}
        if str(body.get("sign", "")).lower() in ruled_signs:
            total += 8
            matched_features.append("planet_in_ruled_sign")
            receipts.append(f"{_format_planet(planet)} is in one of its own signs. Dignity: annoying but relevant.")

    if planet in OUTER_PLANETS:
        personalizers = {"angular_house", "angle_aspect", "core_point_aspect", "personal_aspect_stack", "natural_house", "house_theme"}
        if not personalizers.intersection(matched_features):
            total = min(total, 34)
            receipts.append(
                f"{_format_planet(planet)} is a generational planet, so its sign alone is treated as background weather, not a personality verdict."
            )

    unique_receipts = []
    for receipt in receipts:
        if receipt not in unique_receipts:
            unique_receipts.append(receipt)

    return {
        "code": planet,
        "label": copy["label"],
        "viral_alias": copy["viral_alias"],
        "result_badge": copy["badge"],
        "headline": copy["headline"],
        "score": min(total, 100),
        "placement": _format_placement(body),
        "matched_features": list(dict.fromkeys(matched_features)),
        "receipts": unique_receipts[:5],
    }


def _dominant_element_and_modality(chart: Dict[str, Any]) -> Tuple[str | None, str | None]:
    element_counts: Dict[str, int] = {}
    modality_counts: Dict[str, int] = {}
    for point in ["sun", "moon", "mercury", "venus", "mars", "asc"]:
        body = _get_body(chart, point)
        if not body:
            continue
        sign = str(body.get("sign", "")).lower()
        element = SIGN_ELEMENTS.get(sign)
        modality = SIGN_MODALITIES.get(sign)
        if element:
            element_counts[element] = element_counts.get(element, 0) + 1
        if modality:
            modality_counts[modality] = modality_counts.get(modality, 0) + 1

    element_order = ["fire", "earth", "air", "water"]
    modality_order = ["cardinal", "fixed", "mutable"]
    element = max(element_order, key=lambda item: element_counts.get(item, 0)) if element_counts else None
    modality = max(modality_order, key=lambda item: modality_counts.get(item, 0)) if modality_counts else None
    return element, modality


def _build_signatures(chart: Dict[str, Any], features: Dict[str, Any], top_planets: List[Dict[str, Any]]) -> List[str]:
    signatures: List[str] = []
    top_codes = [planet["code"] for planet in top_planets]
    primary_code = top_codes[0] if top_codes else None

    primary_aspects = []
    if primary_code:
        for aspect in chart.get("aspects", []):
            p1 = str(aspect.get("p1", "")).lower()
            p2 = str(aspect.get("p2", "")).lower()
            if primary_code in {p1, p2}:
                other = p2 if p1 == primary_code else p1
                if other in set(top_codes[1:] + ["north_node", "asc", "mc"]):
                    primary_aspects.append(aspect)

    for aspect in sorted(primary_aspects, key=lambda item: float(item.get("orb", 999)))[:3]:
        signatures.append(_aspect_label(aspect))

    for aspect in chart.get("aspects", []):
        p1 = str(aspect.get("p1", "")).lower()
        p2 = str(aspect.get("p2", "")).lower()
        if (p1 in top_codes or p2 in top_codes) and (p1 in PERSONAL_POINTS or p2 in PERSONAL_POINTS):
            signatures.append(_aspect_label(aspect))
        if len(signatures) >= 3:
            break

    house_names = {
        "first_house_emphasis": "1st-House Emphasis",
        "second_house_emphasis": "2nd-House Emphasis",
        "third_house_emphasis": "3rd-House Emphasis",
        "fourth_house_emphasis": "4th-House Emphasis",
        "fifth_house_emphasis": "5th-House Emphasis",
        "sixth_house_emphasis": "6th-House Emphasis",
        "seventh_house_emphasis": "7th-House Emphasis",
        "eighth_house_emphasis": "8th-House Emphasis",
        "ninth_house_emphasis": "9th-House Emphasis",
        "tenth_house_emphasis": "10th-House Emphasis",
        "twelfth_house_emphasis": "12th-House Emphasis",
    }
    for feature, label in house_names.items():
        if int(features.get(feature, 0) or 0) >= 2:
            signatures.append(label)
        if len(list(dict.fromkeys(signatures))) >= 4:
            break

    return list(dict.fromkeys(signatures))[:4]


def _build_receipts(primary: Dict[str, Any], chart: Dict[str, Any]) -> str:
    planet = str(primary["code"])
    body = _get_body(chart, planet)

    if planet == "venus" and body:
        house = int(body.get("house") or 0)
        house_label = _format_house(house).lower()
        first = (
            f"Venus sits in the {ORDINAL_HOUSES.get(house, str(house) + 'th')} house, one of the chart's angular houses, "
            "so its themes are difficult to hide. Relationships, attraction, taste, and personal values tend to become major arenas of development."
            if house in ANGULAR_HOUSES
            else f"Venus sits in the {house_label}, making relationships, attraction, taste, and personal values major arenas of development."
        )
        venus_contacts = []
        for target in ["uranus", "neptune", "north_node"]:
            if _find_aspects(chart, "venus", {target}, MAJOR_ASPECTS, 6):
                venus_contacts.append(_format_planet(target))

        if venus_contacts:
            if len(venus_contacts) == 1:
                contact_text = venus_contacts[0]
            else:
                contact_text = f"{', '.join(venus_contacts[:-1])}, and {venus_contacts[-1]}"
            second = (
                f"Its contacts with {contact_text} make the Venus story louder: attraction may arrive suddenly, "
                "ideals can outrun reality, and relationships rarely feel emotionally neutral."
            )
        else:
            second = (
                "The Venus story is loud enough on its own: attraction, loyalty, beauty, and value keep asking to be handled consciously."
            )

        return (
            f"{first}\n\n{second}\n\n"
            "In plain English: your love life does not enter quietly. It kicks the door open wearing expensive perfume."
        )

    receipts = primary.get("receipts") or ["The chart kept the evidence subtle. Suspiciously tasteful, but allowed."]
    return " ".join(receipts[:4])


def _build_sections(
    primary: Dict[str, Any],
    top_planets: List[Dict[str, Any]],
    chart_ruler: str | None,
    signatures: List[str],
    chart: Dict[str, Any],
) -> Dict[str, str]:
    ruler_text = _format_planet(chart_ruler) if chart_ruler else "Unknown"
    loudest = " / ".join(_format_planet(item["code"]) for item in top_planets[:3])
    outer_note = (
        "Uranus, Neptune, and Pluto are scored as personal only when they hit angles, personal planets, houses, or repeating themes. Their sign placement alone stays background weather."
    )

    if primary["code"] == "venus":
        real_life = VENUS_REAL_LIFE
        gift = VENUS_GIFT
        damage = VENUS_DAMAGE
        verdict = VENUS_VERDICT
    else:
        real_life = (
            f"You are {primary['viral_alias']}. Dominant planet: {_format_planet(primary['code'])}. "
            f"Chart ruler: {ruler_text}. This planet describes the behavior pattern that keeps showing up before you have had time to make it sound reasonable."
        )
        gift = f"When this signature is grounded, {primary['label']} gives you a clear instinct for where your attention, effort, and timing belong."
        damage = f"The damage starts when {primary['result_badge']} stops being a pattern you can use and becomes an excuse you keep redecorating."
        verdict = PLANET_COPY[primary["code"]]["advice"]

    return {
        "real_life": real_life,
        "the_gift": gift,
        "the_damage": damage,
        "the_receipts": _build_receipts(primary, chart),
        "signature_details": (
            f"Loudest planets: {loudest}. These are the types to follow in forecasts. "
            f"Signatures: {', '.join(signatures) if signatures else 'subtle chart noise with plausible deniability'}. {outer_note}"
        ),
        "grandmothers_verdict": verdict,
    }


def build_planetary_reading_result(
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
    features = extract_features(chart)
    chart_ruler = _get_chart_ruler(chart)

    scored = [_score_planet(planet, chart, features, chart_ruler) for planet in PLANETS]
    scored.sort(key=lambda item: item["score"], reverse=True)
    primary = scored[0]
    loudest = scored[:3]
    signatures = _build_signatures(chart, features, loudest)

    return {
        "service": "planetary_type_reading",
        "primary_planet_type": primary,
        "chart_ruler": {
            "code": chart_ruler,
            "label": _format_planet(chart_ruler) if chart_ruler else "Unknown",
            "placement": _format_placement(_get_body(chart, chart_ruler)) if chart_ruler else "Unknown",
            "ruler_of": _title(chart["angles"]["asc"]["sign"]) if chart.get("angles", {}).get("asc") else "Ascendant",
        },
        "dominant_planet": primary,
        "loudest_planets": loudest,
        "signatures": signatures,
        "section_titles": {
            "real_life": "How This Shows Up in Real Life",
            "the_gift": "The Gift",
            "the_damage": "The Damage",
            "the_receipts": "The Receipts",
            "signature_details": "Detailed Signatures",
            "grandmothers_verdict": "Grandmother's Verdict",
        },
        "sections": _build_sections(primary, loudest, chart_ruler, signatures, chart),
        "all_planet_scores": {item["code"]: item for item in scored},
        "features": features,
        "chart": chart,
    }
