"""The audit's check of the sub-scopes the skills' shared code holds a copy of: the table they are copied from names
the same sub-scopes in the same order."""
import pytest

from audit_set import messages, scope, spec_checks

pytestmark = [pytest.mark.reads("audit-sub-scopes.md", "sub-scopes-of-five", "sub-scopes-of-four", "reviews-without-sub-scopes"),
              pytest.mark.reads("audit-index-chains.md", "index-of-specs-holding-a-methodology",
                                "index-of-a-methodology-holding-a-workflow-folder", "index-of-a-workflow-folder-holding-reviews")]
REVIEWS = "specs/methodology/design-workflow/designs-reviews.md"
INDEXED = {"index-of-specs-holding-a-methodology": "specs/index.md",
           "index-of-a-methodology-holding-a-workflow-folder": "specs/methodology/index.md",
           "index-of-a-workflow-folder-holding-reviews": "specs/methodology/design-workflow/index.md"}


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_a_table_naming_the_sub_scopes_the_code_holds_passes(fixtures):
    assert spec_checks.sub_scope_findings(scope(fixtures, dict(INDEXED, **{"sub-scopes-of-five": REVIEWS}))) == []


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key, message", [
    ("sub-scopes-of-four", "the Sub-scopes table names ['core-canon', 'skills', 'application-specs', 'documentation'], not the "
                           "sub-scopes the scripts read, ['core-canon', 'skills', 'application-specs', 'documentation', 'other']"),
    ("reviews-without-sub-scopes", "the Sub-scopes table is missing"),
])
def test_a_table_out_of_step_with_the_code_is_reported(fixtures, key, message):
    assert messages(spec_checks.sub_scope_findings(scope(fixtures, dict(INDEXED, **{key: REVIEWS})))) == [message]
