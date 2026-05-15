FEATURE_DEFINITIONS = {
    "saturn_angular": {
        "description": "Saturn is placed in an angular house (1, 4, 7, 10).",
        "type": "boolean",
        "logic_hint": {
            "planet": "saturn",
            "houses": [1, 4, 7, 10],
        },
    },
    "saturn_sun_hard": {
        "description": "Saturn forms a hard aspect to the Sun.",
        "type": "boolean",
        "logic_hint": {
            "p1": "saturn",
            "p2": "sun",
            "aspects": ["conjunction", "square", "opposition"],
            "max_orb": 6,
        },
    },
    "saturn_moon_hard": {
        "description": "Saturn forms a hard aspect to the Moon.",
        "type": "boolean",
        "logic_hint": {
            "p1": "saturn",
            "p2": "moon",
            "aspects": ["conjunction", "square", "opposition"],
            "max_orb": 6,
        },
    },
    "saturn_asc_hard": {
        "description": "Saturn strongly aspects the Ascendant.",
        "type": "boolean",
        "logic_hint": {
            "p1": "saturn",
            "p2": "asc",
            "aspects": ["conjunction", "square", "opposition"],
            "max_orb": 5,
        },
    },
    "capricorn_emphasis": {
        "description": "Capricorn is strongly emphasized in the chart.",
        "type": "score",
        "logic_hint": {
            "sign": "capricorn",
            "planets_weighted": ["sun", "moon", "asc", "mercury", "venus", "mars", "saturn"],
        },
    },
    "tenth_house_emphasis": {
        "description": "The 10th house is strongly emphasized.",
        "type": "score",
        "logic_hint": {
            "house": 10,
            "planets_weighted": ["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn", "pluto"],
        },
    },
    "sixth_house_emphasis": {
        "description": "The 6th house is strongly emphasized.",
        "type": "score",
        "logic_hint": {
            "house": 6,
            "planets_weighted": ["sun", "moon", "mercury", "venus", "mars", "saturn"],
        },
    },
    "hard_aspect_dominance": {
        "description": "The chart contains a high proportion of hard aspects overall.",
        "type": "score",
        "logic_hint": {
            "aspects": ["square", "opposition", "conjunction"],
            "mode": "overall_density",
        },
    },
    "uranus_angular": {
        "description": "Uranus is placed in an angular house.",
        "type": "boolean",
        "logic_hint": {
            "planet": "uranus",
            "houses": [1, 4, 7, 10],
        },
    },
    "uranus_moon_hard": {
        "description": "Uranus forms a hard aspect to the Moon.",
        "type": "boolean",
        "logic_hint": {
            "p1": "uranus",
            "p2": "moon",
            "aspects": ["conjunction", "square", "opposition"],
            "max_orb": 6,
        },
    },
    "uranus_mercury_hard": {
        "description": "Uranus forms a hard aspect to Mercury.",
        "type": "boolean",
        "logic_hint": {
            "p1": "uranus",
            "p2": "mercury",
            "aspects": ["conjunction", "square", "opposition"],
            "max_orb": 6,
        },
    },
    "uranus_asc_hard": {
        "description": "Uranus strongly aspects the Ascendant.",
        "type": "boolean",
        "logic_hint": {
            "p1": "uranus",
            "p2": "asc",
            "aspects": ["conjunction", "square", "opposition"],
            "max_orb": 5,
        },
    },
    "mutable_dominance": {
        "description": "Mutable signs are dominant in the chart.",
        "type": "score",
        "logic_hint": {
            "mode": "element_or_modality_count",
            "modality": "mutable",
        },
    },
    "eighth_house_emphasis": {
        "description": "The 8th house is strongly emphasized.",
        "type": "score",
        "logic_hint": {
            "house": 8,
            "planets_weighted": ["sun", "moon", "mercury", "venus", "mars", "pluto", "neptune"],
        },
    },
    "sudden_change_signature": {
        "description": "The chart shows strong markers of sudden change and instability.",
        "type": "score",
        "logic_hint": {
            "combines": ["uranus_angular", "uranus_moon_hard", "uranus_mercury_hard", "mutable_dominance"],
        },
    },
    "mercury_angular": {
        "description": "Mercury is placed in an angular house.",
        "type": "boolean",
        "logic_hint": {
            "planet": "mercury",
            "houses": [1, 4, 7, 10],
        },
    },
    "mercury_sun_close": {
        "description": "Mercury is closely conjunct the Sun.",
        "type": "boolean",
        "logic_hint": {
            "p1": "mercury",
            "p2": "sun",
            "aspects": ["conjunction"],
            "max_orb": 4,
        },
    },
    "mercury_saturn_hard": {
        "description": "Mercury forms a hard aspect to Saturn.",
        "type": "boolean",
        "logic_hint": {
            "p1": "mercury",
            "p2": "saturn",
            "aspects": ["conjunction", "square", "opposition"],
            "max_orb": 6,
        },
    },
    "mercury_neptune_hard": {
        "description": "Mercury forms a tense aspect to Neptune.",
        "type": "boolean",
        "logic_hint": {
            "p1": "mercury",
            "p2": "neptune",
            "aspects": ["conjunction", "square", "opposition"],
            "max_orb": 6,
        },
    },
    "gemini_emphasis": {
        "description": "Gemini is strongly emphasized in the chart.",
        "type": "score",
        "logic_hint": {
            "sign": "gemini",
            "planets_weighted": ["sun", "moon", "asc", "mercury", "venus", "mars"],
        },
    },
    "virgo_emphasis": {
        "description": "Virgo is strongly emphasized in the chart.",
        "type": "score",
        "logic_hint": {
            "sign": "virgo",
            "planets_weighted": ["sun", "moon", "asc", "mercury", "venus", "mars"],
        },
    },
    "third_house_emphasis": {
        "description": "The 3rd house is strongly emphasized.",
        "type": "score",
        "logic_hint": {
            "house": 3,
            "planets_weighted": ["sun", "moon", "mercury", "venus", "mars"],
        },
    },
    "air_dominance": {
        "description": "Air signs are dominant in the chart.",
        "type": "score",
        "logic_hint": {
            "mode": "element_or_modality_count",
            "element": "air",
        },
    },
    "venus_pluto_hard": {
        "description": "Venus forms a hard aspect to Pluto.",
        "type": "boolean",
        "logic_hint": {
            "p1": "venus",
            "p2": "pluto",
            "aspects": ["conjunction", "square", "opposition"],
            "max_orb": 5,
        },
    },
    "moon_pluto_hard": {
        "description": "Moon forms a hard aspect to Pluto.",
        "type": "boolean",
        "logic_hint": {
            "p1": "moon",
            "p2": "pluto",
            "aspects": ["conjunction", "square", "opposition"],
            "max_orb": 5,
        },
    },
    "mars_pluto_hard": {
        "description": "Mars forms a hard aspect to Pluto.",
        "type": "boolean",
        "logic_hint": {
            "p1": "mars",
            "p2": "pluto",
            "aspects": ["conjunction", "square", "opposition"],
            "max_orb": 5,
        },
    },
    "scorpio_emphasis": {
        "description": "Scorpio is strongly emphasized in the chart.",
        "type": "score",
        "logic_hint": {
            "sign": "scorpio",
            "planets_weighted": ["sun", "moon", "asc", "venus", "mars", "pluto"],
        },
    },
    "fifth_house_emphasis": {
        "description": "The 5th house is strongly emphasized.",
        "type": "score",
        "logic_hint": {
            "house": 5,
            "planets_weighted": ["sun", "moon", "venus", "mars", "jupiter"],
        },
    },
    "seventh_house_emphasis": {
        "description": "The 7th house is strongly emphasized.",
        "type": "score",
        "logic_hint": {
            "house": 7,
            "planets_weighted": ["sun", "moon", "venus", "mars", "saturn", "pluto"],
        },
    },
    "relationship_intensity_signature": {
        "description": "The chart suggests intense, high-stakes relational patterns.",
        "type": "score",
        "logic_hint": {
            "combines": ["venus_pluto_hard", "moon_pluto_hard", "mars_pluto_hard", "seventh_house_emphasis", "eighth_house_emphasis"],
        },
    },
    "neptune_angular": {
        "description": "Neptune is placed in an angular house.",
        "type": "boolean",
        "logic_hint": {
            "planet": "neptune",
            "houses": [1, 4, 7, 10],
        },
    },
    "moon_neptune_strong": {
        "description": "Moon and Neptune are strongly connected.",
        "type": "boolean",
        "logic_hint": {
            "p1": "moon",
            "p2": "neptune",
            "aspects": ["conjunction", "square", "opposition", "trine"],
            "max_orb": 6,
        },
    },
    "sun_neptune_strong": {
        "description": "Sun and Neptune are strongly connected.",
        "type": "boolean",
        "logic_hint": {
            "p1": "sun",
            "p2": "neptune",
            "aspects": ["conjunction", "square", "opposition", "trine"],
            "max_orb": 6,
        },
    },
    "asc_neptune_strong": {
        "description": "Neptune strongly aspects the Ascendant.",
        "type": "boolean",
        "logic_hint": {
            "p1": "neptune",
            "p2": "asc",
            "aspects": ["conjunction", "square", "opposition", "trine"],
            "max_orb": 5,
        },
    },
    "twelfth_house_emphasis": {
        "description": "The 12th house is strongly emphasized.",
        "type": "score",
        "logic_hint": {
            "house": 12,
            "planets_weighted": ["sun", "moon", "mercury", "venus", "mars", "neptune"],
        },
    },
    "pisces_emphasis": {
        "description": "Pisces is strongly emphasized in the chart.",
        "type": "score",
        "logic_hint": {
            "sign": "pisces",
            "planets_weighted": ["sun", "moon", "asc", "venus", "mars", "neptune"],
        },
    },
    "water_dominance": {
        "description": "Water signs are dominant in the chart.",
        "type": "score",
        "logic_hint": {
            "mode": "element_or_modality_count",
            "element": "water",
        },
    },
    "porous_boundary_signature": {
        "description": "The chart suggests emotional permeability, blurred boundaries, and dreamlike sensitivity.",
        "type": "score",
        "logic_hint": {
            "combines": ["neptune_angular", "moon_neptune_strong", "twelfth_house_emphasis", "pisces_emphasis", "water_dominance"],
        },
    },
    "north_node_sun_strong": {
        "description": "North Node is strongly connected to the Sun.",
        "type": "boolean",
        "logic_hint": {
            "p1": "north_node",
            "p2": "sun",
            "aspects": ["conjunction", "trine", "sextile"],
            "max_orb": 5,
        },
    },
    "north_node_moon_strong": {
        "description": "North Node is strongly connected to the Moon.",
        "type": "boolean",
        "logic_hint": {
            "p1": "north_node",
            "p2": "moon",
            "aspects": ["conjunction", "trine", "sextile"],
            "max_orb": 5,
        },
    },
    "north_node_asc_strong": {
        "description": "North Node is strongly connected to the Ascendant.",
        "type": "boolean",
        "logic_hint": {
            "p1": "north_node",
            "p2": "asc",
            "aspects": ["conjunction", "trine", "sextile"],
            "max_orb": 5,
        },
    },
    "north_node_mc_strong": {
        "description": "North Node is strongly connected to the Midheaven.",
        "type": "boolean",
        "logic_hint": {
            "p1": "north_node",
            "p2": "mc",
            "aspects": ["conjunction", "trine", "sextile"],
            "max_orb": 5,
        },
    },
    "jupiter_mc_strong": {
        "description": "Jupiter is strongly connected to the Midheaven.",
        "type": "boolean",
        "logic_hint": {
            "p1": "jupiter",
            "p2": "mc",
            "aspects": ["conjunction", "trine", "sextile"],
            "max_orb": 5,
        },
    },
    "saturn_node_strong": {
        "description": "Saturn is strongly connected to the North Node.",
        "type": "boolean",
        "logic_hint": {
            "p1": "saturn",
            "p2": "north_node",
            "aspects": ["conjunction", "square", "opposition", "trine", "sextile"],
            "max_orb": 5,
        },
    },
    "pluto_node_strong": {
        "description": "Pluto is strongly connected to the North Node.",
        "type": "boolean",
        "logic_hint": {
            "p1": "pluto",
            "p2": "north_node",
            "aspects": ["conjunction", "square", "opposition", "trine", "sextile"],
            "max_orb": 5,
        },
    },
    "late_bloomer_signature": {
        "description": "The chart suggests a delayed but significant unfolding of potential.",
        "type": "score",
        "logic_hint": {
            "combines": ["saturn_angular", "north_node_mc_strong", "jupiter_mc_strong", "saturn_node_strong"],
        },
    },
    "mars_angular": {
        "description": "Mars is placed in an angular house.",
        "type": "boolean",
        "logic_hint": {
            "planet": "mars",
            "houses": [1, 4, 7, 10],
        },
    },
    "mars_venus_strong": {
        "description": "Mars and Venus are strongly connected.",
        "type": "boolean",
        "logic_hint": {
            "p1": "mars",
            "p2": "venus",
            "aspects": ["conjunction", "trine", "sextile", "opposition"],
            "max_orb": 5,
        },
    },
    "aries_emphasis": {
        "description": "Aries is strongly emphasized in the chart.",
        "type": "score",
        "logic_hint": {
            "sign": "aries",
            "planets_weighted": ["sun", "moon", "asc", "mars", "venus"],
        },
    },
}