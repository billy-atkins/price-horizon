"""The audit's check of where a blank line falls: one between groups of lines that differ, and none within a group,
as between a sentence and the list it introduces or between the fields of one block."""
import pytest

from audit_set import scope, spec_checks

pytestmark = [pytest.mark.reads("audit-blank-lines.md", "bakery-groups-apart", "bakery-sentence-under-its-title",
                                "bakery-list-apart-from-its-sentence", "bakery-fields-apart")]
BAKERY = "docs/bakery.md"


# @canon-spec specs/methodology/spec-style/markdown.md § Blank Lines
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_blank_lines_between_groups_alone_pass(fixtures):
    held = scope(fixtures, {"bakery-groups-apart": BAKERY})
    assert spec_checks.blank_line_findings(BAKERY, held.text_of[BAKERY], held) == []


# @canon-spec specs/methodology/spec-style/markdown.md § Blank Lines
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key, line, message", [
    ("bakery-sentence-under-its-title", 2, "a blank line missing between a heading and a paragraph"),
    ("bakery-list-apart-from-its-sentence", 4, "a blank line between a paragraph and a list item, where none falls"),
    ("bakery-fields-apart", 4, "a blank line between a field and a field, where none falls"),
])
def test_a_blank_line_out_of_its_place_is_reported(fixtures, key, line, message):
    held = scope(fixtures, {key: BAKERY})
    assert [(n, m) for _, n, m in spec_checks.blank_line_findings(BAKERY, held.text_of[BAKERY], held)] == [(line, message)]
