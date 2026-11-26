"""The construct checks of a configured instance's Held In: an item for each table its construct's form gives, each
naming a fact a Facts record declares whose Type is a list of a context whose entries are the table's columns."""
import pytest

from audit_set import constructs

RULE = "modeling-constructs.md § Constructs § Configured Construct"
WATERING = "specs/garden/watering.md"

pytestmark = [pytest.mark.reads("audit-constructs-held-in.md", "bed-waterings-held-as-data", "bed-waterings-held-in-an-undeclared-fact",
                                "bed-waterings-of-type-string", "bed-waterings-without-a-season", "bed-waterings-held-twice")]


def findings(fixtures, key):
    found, _, _ = constructs.run_checks({WATERING: fixtures[key]})
    return [(rule, line, message) for rule, _, line, message in found]


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Configured Construct
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_a_held_in_naming_a_list_of_the_tables_rows_passes(fixtures):
    assert findings(fixtures, "bed-waterings-held-as-data") == []


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Configured Construct
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key, message", [
    ("bed-waterings-held-in-an-undeclared-fact", "a Held In item citing no Facts record: bed feeds: `§ Facts [Name: bed feeds]`"),
    ("bed-waterings-of-type-string", "a Held In fact whose Type is no list of a context: bed waterings"),
    ("bed-waterings-without-a-season",
     "a Held In fact whose context's entries are not the table's columns: ['soil', 'water'] against ['soil', 'season', 'water']"),
    ("bed-waterings-held-twice", "a Held In giving 2 items for a construct of 1 tables"),
])
def test_a_held_in_out_of_step_with_its_table_is_reported(fixtures, key, message):
    assert [(n, m) for rule, n, m in findings(fixtures, key) if rule == RULE] == [(14, message)]
