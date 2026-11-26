"""The audit's check that no reviewer an agent wrote to set itself up is tracked by version control, a reviewer told
by a file or folder of its path bearing a reviewer's name."""
import pytest

from audit_set import scope, spec_checks

pytestmark = [pytest.mark.reads("audit-reviewers.md", "reviewer-definition", "bakery-readme")]
MESSAGE = "a reviewer definition an agent wrote to set itself up is tracked"


# @canon-spec specs/methodology/scope/agent-agnostic.md § Agent Agnostic
# @canon-spec specs/methodology/skills/setting-up-an-agent.md § Setting Up an Agent
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_a_reviewer_left_untracked_passes(fixtures):
    placed = {"bakery-readme": "README.md", "reviewer-definition": ".agents/review-medium.md"}
    assert spec_checks.reviewer_findings(scope(fixtures, placed, tracked=["README.md"])) == []


# @canon-spec specs/methodology/scope/agent-agnostic.md § Agent Agnostic
# @canon-spec specs/methodology/skills/setting-up-an-agent.md § Setting Up an Agent
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("at", [".agents/review-medium.md", ".agents/review-high/definition.md"])
def test_a_reviewer_tracked_is_reported(fixtures, at):
    placed = {"bakery-readme": "README.md", "reviewer-definition": at}
    assert [f[1:] for f in spec_checks.reviewer_findings(scope(fixtures, placed, tracked=["README.md", at]))] == [(at, 0, MESSAGE)]
