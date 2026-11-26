"""The construct checks of a Name column: a table opens with one exactly where a part of it is cited from outside its
construct's section, only a table that may open one does, and every row gives a Name of its own."""
import pytest

from audit_set import constructs

RULE = "modeling-constructs.md § Constructs § Keyed Construct § Part Identifier"
WATERING = "specs/garden/watering.md"

pytestmark = [pytest.mark.reads("audit-constructs-part-identifiers.md", "watering-need-named-and-cited", "watering-need-named-uncited",
                                "watering-need-name-second", "watering-need-two-rows-named-cold")]


def findings(fixtures, key):
    found, _, _ = constructs.run_checks({WATERING: fixtures[key]})
    return [(rule, line, message) for rule, _, line, message in found]


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Keyed Construct § Part Identifier
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_a_name_column_a_citation_names_a_row_by_passes(fixtures):
    assert findings(fixtures, "watering-need-named-and-cited") == []


# @canon-spec specs/methodology/modeling-constructs.md § Constructs § Keyed Construct § Part Identifier
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key, line, message", [
    ("watering-need-named-uncited", 7, "a Name column no citation from outside its section names a part by: § Watering Need"),
    ("watering-need-name-second", 13, "a column headed Name that does not open a table it may open"),
    ("watering-need-two-rows-named-cold", 13, "a Name column with a row unnamed, or two rows sharing a Name"),
])
def test_a_name_column_out_of_its_place_is_reported(fixtures, key, line, message):
    assert [(n, m) for rule, n, m in findings(fixtures, key) if rule == RULE] == [(line, message)]
