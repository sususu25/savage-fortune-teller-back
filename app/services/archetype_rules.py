ARCHETYPE_RULES = {
    "burdened_one": {
        "label": "The Burdened One",
        "core_features": [
            "saturn_angular",
            "saturn_sun_hard",
            "saturn_moon_hard",
            "saturn_asc_hard",
            "capricorn_emphasis",
            "tenth_house_emphasis",
            "sixth_house_emphasis",
            "hard_aspect_dominance",
        ],
        "weights": {
            "saturn_angular": 20,
            "saturn_sun_hard": 15,
            "saturn_moon_hard": 15,
            "saturn_asc_hard": 15,
            "capricorn_emphasis": 10,
            "tenth_house_emphasis": 10,
            "sixth_house_emphasis": 8,
            "hard_aspect_dominance": 7,
        },
        "secondary_tags": [
            "saturn_heavy"
        ]
    },
    "chaos_magnet": {
        "label": "The Chaos Magnet",
        "core_features": [
            "uranus_angular",
            "uranus_moon_hard",
            "uranus_mercury_hard",
            "uranus_asc_hard",
            "mutable_dominance",
            "eighth_house_emphasis",
            "sudden_change_signature",
        ],
        "weights": {
            "uranus_angular": 18,
            "uranus_moon_hard": 15,
            "uranus_mercury_hard": 14,
            "uranus_asc_hard": 14,
            "mutable_dominance": 12,
            "eighth_house_emphasis": 10,
            "sudden_change_signature": 17,
        },
        "secondary_tags": [
            "eighth_house"
        ]
    },
    "overthinker": {
        "label": "The Overthinker",
        "core_features": [
            "mercury_angular",
            "mercury_sun_close",
            "mercury_saturn_hard",
            "mercury_neptune_hard",
            "gemini_emphasis",
            "virgo_emphasis",
            "third_house_emphasis",
            "sixth_house_emphasis",
            "air_dominance",
        ],
        "weights": {
            "mercury_angular": 16,
            "mercury_sun_close": 10,
            "mercury_saturn_hard": 14,
            "mercury_neptune_hard": 12,
            "gemini_emphasis": 10,
            "virgo_emphasis": 10,
            "third_house_emphasis": 10,
            "sixth_house_emphasis": 8,
            "air_dominance": 10,
        },
        "secondary_tags": [
            "mercury_heavy"
        ]
    },
    "dangerous_heart": {
        "label": "The Dangerous Heart",
        "core_features": [
            "venus_pluto_hard",
            "moon_pluto_hard",
            "mars_pluto_hard",
            "eighth_house_emphasis",
            "scorpio_emphasis",
            "fifth_house_emphasis",
            "seventh_house_emphasis",
            "relationship_intensity_signature",
        ],
        "weights": {
            "venus_pluto_hard": 15,
            "moon_pluto_hard": 15,
            "mars_pluto_hard": 12,
            "eighth_house_emphasis": 14,
            "scorpio_emphasis": 12,
            "fifth_house_emphasis": 8,
            "seventh_house_emphasis": 8,
            "relationship_intensity_signature": 16,
        },
        "secondary_tags": [
            "mars_dominant",
            "eighth_house"
        ]
    },
    "haunted_dreamer": {
        "label": "The Haunted Dreamer",
        "core_features": [
            "neptune_angular",
            "moon_neptune_strong",
            "sun_neptune_strong",
            "asc_neptune_strong",
            "twelfth_house_emphasis",
            "pisces_emphasis",
            "water_dominance",
            "porous_boundary_signature",
        ],
        "weights": {
            "neptune_angular": 18,
            "moon_neptune_strong": 16,
            "sun_neptune_strong": 12,
            "asc_neptune_strong": 12,
            "twelfth_house_emphasis": 16,
            "pisces_emphasis": 10,
            "water_dominance": 8,
            "porous_boundary_signature": 18,
        },
        "secondary_tags": [
            "twelfth_house"
        ]
    },
    "unfinished_legend": {
        "label": "The Unfinished Legend",
        "core_features": [
            "north_node_sun_strong",
            "north_node_moon_strong",
            "north_node_asc_strong",
            "north_node_mc_strong",
            "tenth_house_emphasis",
            "jupiter_mc_strong",
            "saturn_node_strong",
            "pluto_node_strong",
            "late_bloomer_signature",
        ],
        "weights": {
            "north_node_sun_strong": 12,
            "north_node_moon_strong": 12,
            "north_node_asc_strong": 12,
            "north_node_mc_strong": 15,
            "tenth_house_emphasis": 10,
            "jupiter_mc_strong": 10,
            "saturn_node_strong": 10,
            "pluto_node_strong": 8,
            "late_bloomer_signature": 11,
        },
        "secondary_tags": [
            "north_node"
        ]
    }
}


SECONDARY_TAG_RULES = {
    "saturn_heavy": {
        "label": "Saturn-heavy chart",
        "weights": {
            "saturn_angular": 30,
            "saturn_sun_hard": 20,
            "saturn_moon_hard": 20,
            "saturn_asc_hard": 20,
            "capricorn_emphasis": 10,
        }
    },
    "mars_dominant": {
        "label": "Mars-dominant type",
        "weights": {
            "mars_angular": 30,
            "mars_pluto_hard": 20,
            "mars_venus_strong": 15,
            "aries_emphasis": 15,
            "scorpio_emphasis": 20,
        }
    },
    "mercury_heavy": {
        "label": "Mercury-heavy mind",
        "weights": {
            "mercury_angular": 30,
            "mercury_sun_close": 15,
            "mercury_saturn_hard": 15,
            "mercury_neptune_hard": 10,
            "gemini_emphasis": 15,
            "virgo_emphasis": 15,
        }
    },
    "eighth_house": {
        "label": "8th house person",
        "weights": {
            "eighth_house_emphasis": 40,
            "scorpio_emphasis": 20,
            "venus_pluto_hard": 15,
            "moon_pluto_hard": 15,
            "pluto_node_strong": 10,
        }
    },
    "twelfth_house": {
        "label": "12th house placement",
        "weights": {
            "twelfth_house_emphasis": 40,
            "neptune_angular": 15,
            "moon_neptune_strong": 20,
            "pisces_emphasis": 15,
            "porous_boundary_signature": 10,
        }
    },
    "north_node": {
        "label": "North Node person",
        "weights": {
            "north_node_sun_strong": 20,
            "north_node_moon_strong": 20,
            "north_node_asc_strong": 20,
            "north_node_mc_strong": 20,
            "saturn_node_strong": 10,
            "pluto_node_strong": 10,
        }
    }
}