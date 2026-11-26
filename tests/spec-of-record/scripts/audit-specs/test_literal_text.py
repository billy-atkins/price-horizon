"""The audit's check of literal text: a code span opens and closes with one backtick, but a citation whose text holds
a backtick, which takes one more than its longest run, and a fenced or indented code block is left aside."""
import pytest

from audit_set import spec_checks

pytestmark = [pytest.mark.reads("audit-literal-text.md", "literal-text-in-single-backticks", "literal-text-in-double-backticks",
                                "literal-text-citation-in-double-backticks")]


# @canon-spec specs/methodology/spec-style/markdown.md § Literal Text
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_literal_text_in_single_backticks_passes(fixtures):
    assert spec_checks.literal_text_findings("specs/bakery.md", fixtures["literal-text-in-single-backticks"]) == []


# @canon-spec specs/methodology/spec-style/markdown.md § Literal Text
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key", ["literal-text-in-double-backticks", "literal-text-citation-in-double-backticks"])
def test_a_run_of_backticks_is_reported(fixtures, key):
    assert [(line, message) for _, line, message in spec_checks.literal_text_findings("specs/bakery.md", fixtures[key])] == [
        (5, "a run of backticks, where literal text opens and closes with one")]
