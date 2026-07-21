from __future__ import annotations

from typing import Any, Dict, List, Tuple

from app.services.chart_calculator import calculate_chart
from app.services.feature_extractor import extract_features


THEME_CONFIGS: Dict[str, Dict[str, Any]] = {
    "money": {
        "service": "money_curse_reading",
        "primary_key": "primary_money_type",
        "score_key": "all_money_scores",
        "section_titles": {
            "financial_diagnosis": "Financial Diagnosis",
            "the_receipts": "The Receipts",
            "money_pattern": "Money Pattern",
            "spending_hazard": "Spending Hazard",
            "court_ordered_advice": "Court-Ordered Advice",
        },
        "focus_points": ["venus", "jupiter", "saturn"],
        "archetypes": {
            "luxury_denialist": {
                "label": "The Luxury Denialist",
                "viral_alias": "The Budget Has Left The Chat",
                "badge": "aesthetic overspending",
                "headline": "Your taste has a penthouse and your bank account is holding a clipboard in the lobby.",
                "weights": {
                    "venus_angular": 18,
                    "venus_jupiter_easy": 18,
                    "taurus_emphasis": 12,
                    "libra_emphasis": 10,
                    "second_house_emphasis": 16,
                    "jupiter_angular": 12,
                },
            },
            "scarcity_accountant": {
                "label": "The Scarcity Accountant",
                "viral_alias": "The Emergency Fund With Anxiety",
                "badge": "financial hypervigilance",
                "headline": "You do not save money. You build a tiny fortress and call it being realistic.",
                "weights": {
                    "saturn_angular": 16,
                    "saturn_venus_hard": 18,
                    "saturn_moon_hard": 14,
                    "capricorn_emphasis": 14,
                    "sixth_house_emphasis": 10,
                    "hard_aspect_dominance": 8,
                },
            },
            "risky_manifestor": {
                "label": "The Risky Manifestor",
                "viral_alias": "The Financial Plot Twist",
                "badge": "optimism with receipts missing",
                "headline": "You call it abundance mindset. The chart calls it a purchase order with fog on it.",
                "weights": {
                    "jupiter_angular": 18,
                    "sagittarius_emphasis": 14,
                    "ninth_house_emphasis": 10,
                    "jupiter_overextension_signature": 20,
                    "fire_dominance": 10,
                    "uranus_angular": 10,
                },
            },
            "control_tower": {
                "label": "The Control Tower",
                "viral_alias": "The Spreadsheet Exorcist",
                "badge": "money control issues",
                "headline": "Your money life wants control, proof, and possibly a password-protected emotional vault.",
                "weights": {
                    "eighth_house_emphasis": 18,
                    "scorpio_emphasis": 16,
                    "venus_pluto_hard": 14,
                    "hard_aspect_dominance": 10,
                    "saturn_angular": 10,
                    "second_house_emphasis": 10,
                },
            },
        },
    },
    "career": {
        "service": "career_villain_arc",
        "primary_key": "primary_career_type",
        "score_key": "all_career_scores",
        "section_titles": {
            "career_diagnosis": "Career Diagnosis",
            "the_receipts": "The Receipts",
            "public_image": "Public Image",
            "workplace_hazard": "Workplace Hazard",
            "court_ordered_advice": "Court-Ordered Advice",
        },
        "focus_points": ["sun", "saturn", "mc"],
        "archetypes": {
            "corporate_prophet": {
                "label": "The Corporate Prophet",
                "viral_alias": "The Meeting That Became A Movement",
                "badge": "vision with volume",
                "headline": "You can turn a small goal into a doctrine before anyone has opened the calendar.",
                "weights": {
                    "jupiter_angular": 18,
                    "sagittarius_emphasis": 14,
                    "ninth_house_emphasis": 12,
                    "sun_jupiter_easy": 14,
                    "fire_dominance": 12,
                    "jupiter_mc_strong": 16,
                },
            },
            "saturn_climber": {
                "label": "The Saturn Climber",
                "viral_alias": "The Promotion With Back Pain",
                "badge": "ambition taxed",
                "headline": "Your career path has stairs, paperwork, and a universe that keeps saying character development.",
                "weights": {
                    "saturn_angular": 18,
                    "capricorn_emphasis": 14,
                    "tenth_house_emphasis": 16,
                    "sixth_house_emphasis": 10,
                    "saturn_sun_hard": 14,
                    "saturn_node_strong": 10,
                },
            },
            "spotlight_problem": {
                "label": "The Spotlight Problem",
                "viral_alias": "The Main Character With Deliverables",
                "badge": "visible and annoyed",
                "headline": "You want recognition, but the chart would like to see the deliverable before the applause.",
                "weights": {
                    "sun_angular": 18,
                    "leo_emphasis": 14,
                    "tenth_house_emphasis": 12,
                    "sun_asc_close": 14,
                    "fire_dominance": 10,
                    "fifth_house_emphasis": 8,
                },
            },
            "behind_scenes_operator": {
                "label": "The Behind-The-Scenes Operator",
                "viral_alias": "The Power Behind The Curtain",
                "badge": "private influence",
                "headline": "You may not need the stage. You need the lever nobody noticed you were holding.",
                "weights": {
                    "twelfth_house_emphasis": 16,
                    "eighth_house_emphasis": 14,
                    "neptune_angular": 12,
                    "scorpio_emphasis": 10,
                    "asc_ruler_hard": 12,
                    "water_dominance": 8,
                },
            },
        },
    },
    "energy": {
        "service": "energy_damage_forecast",
        "primary_key": "primary_energy_type",
        "score_key": "all_energy_scores",
        "section_titles": {
            "energy_diagnosis": "Energy Diagnosis",
            "the_receipts": "The Receipts",
            "stress_pattern": "Stress Pattern",
            "burnout_hazard": "Burnout Hazard",
            "court_ordered_advice": "Court-Ordered Advice",
        },
        "focus_points": ["moon", "mars", "saturn"],
        "archetypes": {
            "nervous_system_ceo": {
                "label": "The Nervous System CEO",
                "viral_alias": "The Burnout With A Calendar",
                "badge": "over-functioning",
                "headline": "You schedule rest like a hostile meeting request and wonder why your body files complaints.",
                "weights": {
                    "saturn_angular": 18,
                    "sixth_house_emphasis": 16,
                    "saturn_moon_hard": 14,
                    "hard_aspect_dominance": 10,
                    "capricorn_emphasis": 12,
                },
            },
            "emotional_sponge": {
                "label": "The Emotional Sponge",
                "viral_alias": "The Group Chat Weather System",
                "badge": "absorbing everything",
                "headline": "Other people's moods keep entering your body like they pay rent.",
                "weights": {
                    "moon_angular": 16,
                    "water_dominance": 16,
                    "moon_neptune_strong": 16,
                    "twelfth_house_emphasis": 14,
                    "porous_boundary_signature": 18,
                    "pisces_emphasis": 10,
                },
            },
            "adrenaline_addict": {
                "label": "The Adrenaline Addict",
                "viral_alias": "The Fight-Or-Also-Fight Response",
                "badge": "urgency disorder",
                "headline": "Your energy system thinks everything is a launch, a duel, or a limited-time offer.",
                "weights": {
                    "mars_angular": 18,
                    "aries_emphasis": 16,
                    "fire_dominance": 14,
                    "moon_mars_hard": 14,
                    "mars_sun_hard": 12,
                    "first_house_emphasis": 8,
                },
            },
            "fog_machine": {
                "label": "The Fog Machine",
                "viral_alias": "The Mystical Low Battery Mode",
                "badge": "dreamy depletion",
                "headline": "Your energy disappears into atmosphere, fantasy, and one tab labeled later.",
                "weights": {
                    "neptune_angular": 18,
                    "sun_neptune_strong": 14,
                    "moon_neptune_strong": 16,
                    "twelfth_house_emphasis": 14,
                    "pisces_emphasis": 12,
                    "mutable_dominance": 8,
                },
            },
        },
    },
}


FEATURE_RECEIPTS = {
    "second_house_emphasis": "2nd-house emphasis makes money, worth, comfort, and security louder than the chart pretends.",
    "eighth_house_emphasis": "8th-house emphasis brings debt, shared resources, control, and psychological invoice energy.",
    "venus_jupiter_easy": "Venus-Jupiter harmony expands pleasure. Lovely in theory, expensive in lighting.",
    "jupiter_overextension_signature": "Jupiter overextension makes 'it will work out' sound like a financial plan.",
    "saturn_venus_hard": "Saturn-Venus tension turns pleasure and money into a permission slip.",
    "venus_angular": "Angular Venus makes taste, desire, comfort, and aesthetic emergencies louder.",
    "taurus_emphasis": "Taurus emphasis wants comfort, stability, quality, and occasionally a receipt from the soul.",
    "libra_emphasis": "Libra emphasis gives taste, comparison, charm, and an invoice for bad lighting.",
    "venus_pluto_hard": "Venus-Pluto tension brings desire, control, and money feelings with suspicious basement lighting.",
    "scorpio_emphasis": "Scorpio emphasis makes shared resources, trust, and emotional leverage hard to ignore.",
    "tenth_house_emphasis": "10th-house emphasis makes reputation and achievement feel impossible to ignore.",
    "sixth_house_emphasis": "6th-house emphasis puts work, routines, labor, and burnout paperwork on the desk.",
    "sun_angular": "Angular Sun makes visibility part of the life assignment.",
    "saturn_angular": "Angular Saturn adds duty, pressure, delays, and suspiciously mature posture.",
    "jupiter_angular": "Angular Jupiter makes ambition, belief, and expansion loud enough for the balcony.",
    "twelfth_house_emphasis": "12th-house emphasis sends energy into private rooms, dreams, avoidance, and background processes.",
    "moon_neptune_strong": "Moon-Neptune contact makes emotional boundaries porous enough to require towels.",
    "moon_mars_hard": "Moon-Mars tension makes moods arrive with a tiny emergency siren.",
    "mars_angular": "Angular Mars puts urgency, pursuit, and conflict in the driver's seat.",
    "hard_aspect_dominance": "Hard aspect dominance means the chart believes friction is a personality workshop.",
    "sun_jupiter_easy": "Sun-Jupiter harmony expands confidence, ambition, and the belief that the room may need your vision.",
    "jupiter_mc_strong": "Jupiter-Midheaven contact makes career appetite larger than the calendar.",
    "sagittarius_emphasis": "Sagittarius emphasis adds belief, reach, teaching energy, and a dangerous tolerance for big claims.",
    "saturn_sun_hard": "Sun-Saturn tension turns ambition into a staircase with emotional toll booths.",
    "saturn_node_strong": "Saturn-Node contact gives the life path homework, deadlines, and very little glitter.",
    "leo_emphasis": "Leo emphasis makes visibility, performance, pride, and recognition part of the job description.",
    "sun_asc_close": "Sun near the Ascendant makes presence hard to miss and harder to mute.",
    "asc_ruler_hard": "A stressed Ascendant ruler makes presentation, identity, and public strategy work overtime.",
    "neptune_angular": "Angular Neptune makes image, imagination, fog, and projection unusually visible.",
    "water_dominance": "Water dominance makes emotional atmosphere part of the operating system.",
    "moon_angular": "Angular Moon puts needs, habits, and moods in the front office.",
    "porous_boundary_signature": "Porous-boundary signatures make other people's weather feel annoyingly downloadable.",
    "pisces_emphasis": "Pisces emphasis adds sensitivity, intuition, drift, and questionable relationships with reality.",
    "aries_emphasis": "Aries emphasis adds heat, speed, initiative, and low patience for slow loading screens.",
    "fire_dominance": "Fire dominance brings urgency, courage, appetite, and occasionally a missing brake pedal.",
    "mars_sun_hard": "Mars-Sun tension turns drive into a competitive sport with dramatic hydration needs.",
    "first_house_emphasis": "1st-house emphasis makes identity, body, and impulse hard to politely hide.",
    "sun_neptune_strong": "Sun-Neptune contact blurs identity, fantasy, compassion, and one suspiciously persuasive playlist.",
    "mutable_dominance": "Mutable dominance adapts fast, changes lanes, and may need a firmer container.",
}


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


def _has_aspect(chart: Dict[str, Any], p1: str, p2: str, aspect_types: set[str], max_orb: float) -> bool:
    p1 = p1.lower()
    p2 = p2.lower()
    for aspect in chart.get("aspects", []):
        a1 = str(aspect.get("p1", "")).lower()
        a2 = str(aspect.get("p2", "")).lower()
        same_pair = (a1 == p1 and a2 == p2) or (a1 == p2 and a2 == p1)
        if same_pair and str(aspect.get("type", "")).lower() in aspect_types and float(aspect.get("orb", 999)) <= max_orb:
            return True
    return False


def _get_body(chart: Dict[str, Any], body_name: str) -> Dict[str, Any] | None:
    if body_name in chart.get("planets", {}):
        return chart["planets"][body_name]
    if body_name in chart.get("angles", {}):
        return chart["angles"][body_name]
    return None


def _theme_features(chart: Dict[str, Any]) -> Dict[str, Any]:
    features = extract_features(chart)
    features["saturn_venus_hard"] = _has_aspect(chart, "saturn", "venus", {"conjunction", "square", "opposition"}, 6)
    return features


def _build_sections(theme: str, primary: Dict[str, Any], matched: List[str], chart: Dict[str, Any]) -> Dict[str, str]:
    config = THEME_CONFIGS[theme]
    receipts = [FEATURE_RECEIPTS.get(feature, feature.replace("_", " ")) for feature in matched[:4]]
    if not receipts:
        receipts = ["The chart kept its evidence subtle. That is not innocence; that is better lighting."]

    focus = []
    for point_name in config["focus_points"]:
        body = _get_body(chart, point_name)
        if body:
            if "house" in body:
                focus.append(f"{point_name.upper()} in {body['sign']} house {body['house']}")
            else:
                focus.append(f"{point_name.upper()} in {body['sign']}")

    if theme == "money":
        return {
            "financial_diagnosis": f"You are {primary['viral_alias']}. Your money pattern is not random; it has taste, fear, timing, and a receipt drawer.",
            "the_receipts": " ".join(receipts),
            "money_pattern": f"Core money signatures: {', '.join(focus)}. Translation: your chart has opinions about comfort, risk, worth, and control.",
            "spending_hazard": "The hazard is treating emotion like a checkout button. Desire is data, not always instruction.",
            "court_ordered_advice": "Make one boring money rule before the next aesthetic emergency. The rule is not a prison; it is a seatbelt with better branding.",
        }

    if theme == "career":
        return {
            "career_diagnosis": f"You are {primary['viral_alias']}. Your career chart wants impact, but it also wants a plot arc and possibly a dramatic chair turn.",
            "the_receipts": " ".join(receipts),
            "public_image": f"Career signatures: {', '.join(focus)}. These show visibility, discipline, ambition, and the flavor of your public self.",
            "workplace_hazard": "The hazard is confusing pressure with purpose. Just because it is heavy does not mean it is holy.",
            "court_ordered_advice": "Pick one visible move and one private system. Your destiny does not need more lore; it needs shipping.",
        }

    return {
        "energy_diagnosis": f"You are {primary['viral_alias']}. This is energy weather, not medical advice, and the forecast is spiritually rude.",
        "the_receipts": " ".join(receipts),
        "stress_pattern": f"Energy signatures: {', '.join(focus)}. These show drive, emotional absorption, pressure, and recovery style.",
        "burnout_hazard": "The hazard is ignoring the body's memo until it sends the same memo in a louder font.",
        "court_ordered_advice": "Reduce one input, name one need, and stop treating rest like a luxury item with a velvet rope.",
    }


def build_themed_reading_result(
    theme: str,
    birth_date: str,
    birth_time: str,
    birth_city: str,
    latitude: float | None = None,
    longitude: float | None = None,
    timezone: str | None = None,
) -> dict:
    if theme not in THEME_CONFIGS:
        raise ValueError(f"Unknown reading theme: {theme}")

    chart = calculate_chart(
        birth_date=birth_date,
        birth_time=birth_time,
        birth_city=birth_city,
        latitude=latitude,
        longitude=longitude,
        timezone=timezone,
    )
    features = _theme_features(chart)
    config = THEME_CONFIGS[theme]

    scored = []
    for code, archetype in config["archetypes"].items():
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
        "service": config["service"],
        config["primary_key"]: primary,
        "section_titles": config["section_titles"],
        "sections": _build_sections(theme, primary, primary["matched_features"], chart),
        config["score_key"]: {item["code"]: item for item in scored},
        "features": features,
        "chart": chart,
    }
