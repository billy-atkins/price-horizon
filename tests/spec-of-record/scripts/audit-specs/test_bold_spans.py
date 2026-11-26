"""The audit's check of bold: a bold span opens a line and closes on a colon, a field in its form, or on a period or a
question mark, a lead-in; bold italic, underscore bold and a dash serving as punctuation are reported wherever they
stand outside code."""
import pytest

from audit_set import spec_checks

pytestmark = [pytest.mark.reads("audit-bold-spans.md", "bold-at-line-openings", "bold-in-a-line-middle",
                                "bold-field-after-an-asterisk-marker", "bold-opening-closing-on-a-word",
                                "bold-prose-with-an-em-dash", "bold-italic-lead-in", "bold-in-underscores")]


# @canon-spec specs/methodology/modeling-constructs.md § Fields
# @canon-spec specs/methodology/spec-style/clear-prose.md § Clear Prose
# @canon-spec specs/methodology/spec-style/markdown.md § Bold Lead-ins
# @canon-spec specs/methodology/spec-style/markdown.md § Emphasis
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_bold_opening_lines_passes(fixtures):
    assert spec_checks.bold_span_findings("specs/bakery.md", fixtures["bold-at-line-openings"]) == []


# @canon-spec specs/methodology/modeling-constructs.md § Fields
# @canon-spec specs/methodology/spec-style/clear-prose.md § Clear Prose
# @canon-spec specs/methodology/spec-style/markdown.md § Bold Lead-ins
# @canon-spec specs/methodology/spec-style/markdown.md § Emphasis
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key, rule, message", [
    ("bold-in-a-line-middle", spec_checks.EMPHASIS, "bold outside a line's opening: **dark**"),
    ("bold-field-after-an-asterisk-marker", spec_checks.FIELDS,
     "a field not in its form, its key in bold, then a space, any list marker a hyphen: **Oven:** Deck"),
    ("bold-opening-closing-on-a-word", spec_checks.BOLD_LEAD_INS,
     "bold opening a line closes on neither a colon nor a period: **Fresh bread**"),
    ("bold-prose-with-an-em-dash", spec_checks.CLEAR_PROSE,
     "an em dash or an en dash, where a sentence takes a period, a comma, a colon or parentheses"),
    ("bold-italic-lead-in", spec_checks.EMPHASIS, "bold italic or underscore bold"),
    ("bold-in-underscores", spec_checks.EMPHASIS, "bold italic or underscore bold"),
])
def test_bold_out_of_its_form_is_reported(fixtures, key, rule, message):
    assert spec_checks.bold_span_findings("specs/bakery.md", fixtures[key]) == [(rule, 3, message)]
