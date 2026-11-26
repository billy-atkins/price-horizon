"""The audit's check of a file's headings: each a plain title, with no number opening it, no section sign and no
bracket, and none standing twice among its siblings."""
import pytest

from audit_set import messages, spec_checks

pytestmark = [pytest.mark.reads("audit-headings.md", "headings-titled-plainly", "heading-numbered", "heading-holding-a-section-sign",
                                "heading-holding-a-bracket", "headings-twice-among-siblings")]


# @canon-spec specs/methodology/sourcing-and-citation/titling-a-heading.md § Titling a Heading
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_headings_titled_plainly_pass(fixtures):
    assert spec_checks.heading_findings("specs/harbor.md", fixtures["headings-titled-plainly"]) == []


# @canon-spec specs/methodology/sourcing-and-citation/titling-a-heading.md § Titling a Heading
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key, message", [
    ("heading-numbered", "heading carries an ordinal: 2. Tides"),
    ("heading-holding-a-section-sign", "heading contains §: Tides § Springs"),
    ("heading-holding-a-bracket", "heading contains [: Tides [Springs]"),
    ("headings-twice-among-siblings", "duplicate heading under The Harbor: Moorings"),
])
def test_a_heading_out_of_its_form_is_reported(fixtures, key, message):
    assert messages(spec_checks.heading_findings("specs/harbor.md", fixtures[key])) == [message]
