"""The construct checks of a Decision Table: one row deciding each case, no case left out, a hit policy DMN names,
each cell within its column's values and each Reads item a name and a citation; and a condition whose kinds only its
table names, listed for the reading audit."""
import pytest

from audit_set import constructs

RULE = "modeling-constructs.md § Constructs § Decision Table"
WATERING = "specs/garden/watering.md"
KINDS = "a condition whose kinds only its table names"

pytestmark = [pytest.mark.reads("audit-constructs-decision-tables.md", "watering-need", "watering-need-two-rows-for-clay-in-summer",
                                "watering-need-without-sand-in-winter", "watering-need-hit-policy-highest",
                                "watering-need-a-loam-row", "watering-need-reads-rainfall-bare", "watering-by-questions")]


def checked(fixtures, key):
    """-> the findings and the candidates of the construct checks over the fixture `key`, standing as the garden's
    watering file."""
    found, _, candidates = constructs.run_checks({WATERING: fixtures[key]})
    return [(rule, line, message) for rule, _, line, message in found], candidates


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Decision Table
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_a_table_deciding_each_case_once_passes(fixtures):
    assert checked(fixtures, "watering-need")[0] == []


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Decision Table
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key, line, message", [
    ("watering-need-two-rows-for-clay-in-summer", 16, "a case two rows match, where the hit policy is Unique"),
    ("watering-need-without-sand-in-winter", 13, "a case no row matches: ('sand', 'winter')"),
    ("watering-need-hit-policy-highest", 8, "a Hit Policy that is none of DMN's: Highest"),
    ("watering-need-a-loam-row", 18, "a cell outside its column's values: soil"),
    ("watering-need-reads-rainfall-bare", 7, "a Reads item that is not a name, a colon and a citation: rainfall"),
])
def test_a_table_out_of_its_checks_is_reported(fixtures, key, line, message):
    assert checked(fixtures, key)[0] == [(RULE, line, message)]


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Decision Table
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_conditions_asked_as_questions_are_not_listed_for_reading(fixtures):
    found, candidates = checked(fixtures, "watering-by-questions")
    assert found == [] and [c for c in candidates if c[2] == KINDS] == []


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Decision Table
@pytest.mark.action("--check-scope")
@pytest.mark.reports
def test_conditions_of_words_only_the_table_names_are_listed_for_reading(fixtures):
    _, candidates = checked(fixtures, "watering-need")
    assert [(line, context) for _, line, pattern, context in candidates if pattern == KINDS] == [
        (7, "§ Watering Need: whether the values of soil hold every kind of case is read, or it is written as the questions defining its kinds"),
        (7, "§ Watering Need: whether the values of season hold every kind of case is read, or it is written as the questions defining its kinds"),
    ]
