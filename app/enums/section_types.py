from enum import Enum


class SectionType(str, Enum):
    INTRO = "intro"
    OVERALL = "overall"
    LOVE = "love"
    CAREER = "career"
    HEALTH = "health"
    MONEY = "money"