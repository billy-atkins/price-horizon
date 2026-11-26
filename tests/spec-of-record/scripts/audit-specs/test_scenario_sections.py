"""The audit's check of acceptance scenarios: a Test Scenarios section stands one level below its capability and holds
a gherkin block, and every scenario of a gherkin block, inside such a section or not, carries a Given, a When and a
Then."""
import pytest

from audit_set import messages, spec_checks

pytestmark = [pytest.mark.reads("audit-scenario-sections.md", "scenarios-one-level-below-their-capability",
                                "scenarios-two-levels-below-their-capability", "scenarios-without-a-gherkin-block",
                                "scenario-without-a-when", "gherkin-outside-scenarios-without-a-given")]


# @canon-spec specs/methodology/acceptance-scenarios.md § Acceptance Scenarios
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_scenarios_in_their_form_pass(fixtures):
    assert spec_checks.scenario_findings("specs/bakery.md", fixtures["scenarios-one-level-below-their-capability"]) == []


# @canon-spec specs/methodology/acceptance-scenarios.md § Acceptance Scenarios
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key, message", [
    ("scenarios-two-levels-below-their-capability", "Test Scenarios is not exactly one level below its capability"),
    ("scenarios-without-a-gherkin-block", "Test Scenarios section has no ```gherkin fence"),
    ("scenario-without-a-when", "scenario has no When: A loaf is ordered"),
    ("gherkin-outside-scenarios-without-a-given", "scenario has no Given: A loaf is ordered"),
])
def test_scenarios_out_of_their_form_are_reported(fixtures, key, message):
    assert messages(spec_checks.scenario_findings("specs/bakery.md", fixtures[key])) == [message]
