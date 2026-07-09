from enum import Enum


class SectionType(str, Enum):
    COSMIC_DIAGNOSIS = "cosmic_diagnosis"
    WHY_YOU_ARE_LIKE_THIS = "why_you_are_like_this"
    THE_RECEIPTS = "the_receipts"
    EMOTIONAL_DAMAGE_FORECAST = "emotional_damage_forecast"
    LOVE_LIFE_A_SITUATION = "love_life_a_situation"
    COURT_ORDERED_ADVICE = "court_ordered_advice"
