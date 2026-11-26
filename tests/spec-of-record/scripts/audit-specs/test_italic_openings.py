"""The audit's check of italic at a line's opening: no line opens with italic, after any list marker, quote marker
and indentation, while italic within a line, a list item an asterisk marks, a code span and a fenced block pass."""
import pytest

from audit_set import spec_checks

pytestmark = [pytest.mark.reads("audit-italic-openings.md", "italic-inside-lines", "italic-opening-a-paragraph",
                                "italic-opening-a-list-item", "italic-opening-a-quote")]


# @canon-spec specs/methodology/spec-style/markdown.md § Emphasis
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_italic_inside_lines_passes(fixtures):
    assert spec_checks.italic_opening_findings("specs/garden.md", fixtures["italic-inside-lines"]) == []


# @canon-spec specs/methodology/spec-style/markdown.md § Emphasis
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key", ["italic-opening-a-paragraph", "italic-opening-a-list-item", "italic-opening-a-quote"])
def test_a_line_opening_with_italic_is_reported(fixtures, key):
    assert [(line, message) for _, line, message in spec_checks.italic_opening_findings("specs/garden.md", fixtures[key])] == [
        (3, "a line opens with italic")]
