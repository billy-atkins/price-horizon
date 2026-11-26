"""The audit's check of the section sign: each stands inside a backtick span, a citation's or any other, and one
outside every span, in prose or in a table, is reported, while a fenced block is left aside."""
import pytest

from audit_set import spec_checks

pytestmark = [pytest.mark.reads("audit-section-signs.md", "section-signs-in-backticks", "section-sign-in-prose",
                                "section-sign-in-a-table-cell")]


# @canon-spec specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_section_signs_in_backticks_pass(fixtures):
    assert spec_checks.loose_section_findings("specs/harbor.md", fixtures["section-signs-in-backticks"]) == []


# @canon-spec specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key", ["section-sign-in-prose", "section-sign-in-a-table-cell"])
def test_a_section_sign_outside_backticks_is_reported(fixtures, key):
    assert [(line, message) for _, line, message in spec_checks.loose_section_findings("specs/harbor.md", fixtures[key])] == [
        (5, "a § outside a backtick span")]
