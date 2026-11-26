"""The construct checks of a construct's block of fields: a field holding a list gives its items beneath its key, and
a Default Output beneath its key gives an item for each of two or more outcome columns."""
import pytest

from audit_set import constructs

RULE = "modeling-constructs.md § Defining Constructs § Declaring a Construct"
WATERING = "specs/garden/watering.md"

pytestmark = [pytest.mark.reads("audit-constructs-decision-tables.md", "watering-need", "watering-need-default-output-on-the-key-line",
                                "watering-need-input-values-on-the-key-line", "watering-need-default-output-one-item")]


def findings(fixtures, key):
    found, _, _ = constructs.run_checks({WATERING: fixtures[key]})
    return [(rule, line, message) for rule, _, line, message in found]


# @canon-spec specs/methodology/modeling-constructs.md § Defining Constructs § Declaring a Construct
@pytest.mark.action("--check-scope")
@pytest.mark.passes
@pytest.mark.parametrize("key", ["watering-need", "watering-need-default-output-on-the-key-line"])
def test_lists_beneath_their_keys_and_one_outcome_on_its_line_pass(fixtures, key):
    assert findings(fixtures, key) == []


# @canon-spec specs/methodology/modeling-constructs.md § Defining Constructs § Declaring a Construct
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key, line, message", [
    ("watering-need-input-values-on-the-key-line", 9, "the Input Values field's list written on its key's line, not beneath it"),
    ("watering-need-default-output-one-item", 12, "a Default Output written beneath its key with fewer than two items"),
])
def test_a_field_written_out_of_its_block_form_is_reported(fixtures, key, line, message):
    assert [(n, m) for rule, n, m in findings(fixtures, key) if rule == RULE] == [(line, message)]
