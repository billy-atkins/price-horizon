"""The audit's check of numbers on lead-ins and list items: no bold lead-in and no list item carries a number, while a
sentence opening with a count and a numbered list in a fenced block pass."""
import pytest

from audit_set import spec_checks

pytestmark = [pytest.mark.reads("audit-numbered-lists.md", "lists-without-numbers", "numbered-bold-lead-in",
                                "numbered-list-item-with-a-period", "numbered-list-item-with-a-parenthesis")]


# @canon-spec specs/methodology/spec-style/ordinals-and-counts.md § Ordinals and Counts
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_lists_without_numbers_pass(fixtures):
    assert spec_checks.numbered_findings("specs/bakery.md", fixtures["lists-without-numbers"]) == []


# @canon-spec specs/methodology/spec-style/ordinals-and-counts.md § Ordinals and Counts
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key, message", [
    ("numbered-bold-lead-in", "bold lead-in carries a number"),
    ("numbered-list-item-with-a-period", "list item carries a number"),
    ("numbered-list-item-with-a-parenthesis", "list item carries a number"),
])
def test_a_number_on_a_lead_in_or_an_item_is_reported(fixtures, key, message):
    assert [(line, m) for _, line, m in spec_checks.numbered_findings("specs/bakery.md", fixtures[key])] == [(3, message)]
