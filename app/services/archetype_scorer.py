from typing import Any, Dict, List, Tuple

from app.services.archetype_rules import ARCHETYPE_RULES, SECONDARY_TAG_RULES


def _score_from_weights(features: Dict[str, Any], weights: Dict[str, int]) -> Tuple[int, List[str]]:
    total_score = 0
    matched_features: List[str] = []

    for feature_name, weight in weights.items():
        value = features.get(feature_name, 0)

        if isinstance(value, bool):
            if value:
                total_score += weight
                matched_features.append(feature_name)

        elif isinstance(value, (int, float)):
            if value > 0:
                total_score += min(int(value), weight)
                matched_features.append(feature_name)

    return min(total_score, 100), matched_features


def calculate_archetype_scores(features: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    results: Dict[str, Dict[str, Any]] = {}

    for archetype_code, rule in ARCHETYPE_RULES.items():
        score, matched_features = _score_from_weights(features, rule["weights"])

        results[archetype_code] = {
            "label": rule["label"],
            "score": score,
            "matched_features": matched_features,
            "secondary_tags": rule.get("secondary_tags", []),
        }

    return results


def calculate_secondary_tag_scores(features: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    results: Dict[str, Dict[str, Any]] = {}

    for tag_code, rule in SECONDARY_TAG_RULES.items():
        score, matched_features = _score_from_weights(features, rule["weights"])

        results[tag_code] = {
            "label": rule["label"],
            "score": score,
            "matched_features": matched_features,
        }

    return results


def get_primary_archetype(archetype_scores: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    primary_code = max(
        archetype_scores,
        key=lambda code: archetype_scores[code]["score"]
    )

    primary_data = archetype_scores[primary_code]

    return {
        "code": primary_code,
        "label": primary_data["label"],
        "score": primary_data["score"],
        "matched_features": primary_data["matched_features"],
        "secondary_tags": primary_data["secondary_tags"],
    }


def get_active_secondary_tags(
    secondary_tag_scores: Dict[str, Dict[str, Any]],
    threshold: int = 20,
) -> List[Dict[str, Any]]:
    active_tags: List[Dict[str, Any]] = []

    for tag_code, tag_data in secondary_tag_scores.items():
        if tag_data["score"] >= threshold:
            active_tags.append(
                {
                    "code": tag_code,
                    "label": tag_data["label"],
                    "score": tag_data["score"],
                    "matched_features": tag_data["matched_features"],
                }
            )

    active_tags.sort(key=lambda item: item["score"], reverse=True)
    return active_tags


def calculate_full_archetype_result(features: Dict[str, Any]) -> Dict[str, Any]:
    archetype_scores = calculate_archetype_scores(features)
    secondary_tag_scores = calculate_secondary_tag_scores(features)

    primary_archetype = get_primary_archetype(archetype_scores)
    active_secondary_tags = get_active_secondary_tags(secondary_tag_scores)

    return {
        "primary_archetype": primary_archetype,
        "archetype_scores": archetype_scores,
        "secondary_tag_scores": secondary_tag_scores,
        "active_secondary_tags": active_secondary_tags,
    }