from app.data.archetype_copy import ARCHETYPE_COPY, SECTION_TITLES, get_archetype_copy
from app.repositories.interpretation_repository import find_interpretations
from app.services.archetype_rules import ARCHETYPE_RULES


def test_all_archetypes_have_viral_copy():
    for type_code in ARCHETYPE_RULES.keys():
        copy = get_archetype_copy(type_code, 76)

        assert copy["viral_alias"]
        assert copy["headline"]
        assert copy["result_badge"]
        assert "76%" in copy["share_text"]


def test_all_archetypes_have_all_result_sections():
    for type_code in ARCHETYPE_RULES.keys():
        sections = find_interpretations(type_code=type_code, score=76)

        assert set(sections.keys()) == set(SECTION_TITLES.keys())
        assert all(sections.values())


def test_copy_catalog_matches_archetypes():
    assert set(ARCHETYPE_COPY.keys()) == set(ARCHETYPE_RULES.keys())
