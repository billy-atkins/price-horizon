"""The audit's check that every section of the methodology is named by a check or by a skipped step, and that each
section a skipped step names as stating operating rules is cited by a step of a registered skill's workflow."""
import pytest

from audit_set import messages, scope, spec_checks

pytestmark = [pytest.mark.reads("audit-coverage.md", "index-of-a-harbor-methodology", "harbor-tides-of-two-sections",
                                "harbor-tides-with-neap-tides", "harbor-moorings-section", "harbor-audits-naming-tides",
                                "harbor-audits-without-enforces", "harbor-skipped-steps", "registry-of-a-mooring-skill",
                                "mooring-skill", "harbor-code-checks"),
              pytest.mark.reads("audit-index-chains.md", "index-of-specs-holding-a-methodology")]
TIDES, AUDITS = "specs/methodology/tides.md", ".ai/skills/audit-specs/SKILL.md"
HARBOUR = {"index-of-specs-holding-a-methodology": "specs/index.md", "index-of-a-harbor-methodology": "specs/methodology/index.md",
           "harbor-tides-of-two-sections": TIDES, "harbor-moorings-section": "specs/methodology/moorings.md",
           "harbor-audits-naming-tides": AUDITS, "harbor-skipped-steps": "specs/methodology/scope/rules-and-skills.md",
           "registry-of-a-mooring-skill": "specs/methodology/skills/registered-skills.md",
           "mooring-skill": ".ai/skills/moor-a-boat/SKILL.md",
           "harbor-code-checks": ".ai/skills/verify-spec-implementation/SKILL.md"}


# @canon-spec specs/methodology/scope/rules-and-skills.md § Rules and Skills
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_sections_each_named_and_operating_rules_each_cited_pass(fixtures):
    assert spec_checks.coverage_findings(scope(fixtures, HARBOUR)) == []


# @canon-spec specs/methodology/scope/rules-and-skills.md § Rules and Skills
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("swapped, left_out, found", [
    ({"harbor-tides-with-neap-tides": TIDES}, None, ["no check or step names § Neap Tides"]),
    ({"harbor-audits-without-enforces": AUDITS}, None,
     ["no Enforces column in a table under ## The audits", "no check or step names § Tides", "no check or step names § Tides § Springs"]),
    ({}, "mooring-skill",
     ["no registered skill's Workflow step cites the section stating operating rules specs/methodology/moorings.md § Moorings"]),
    ({}, "harbor-code-checks", ["no table of the code's checks, so no rule for code is named"]),
])
def test_a_section_no_check_or_step_reaches_is_reported(fixtures, swapped, left_out, found):
    placed = {k: p for k, p in HARBOUR.items() if p not in swapped.values() and k != left_out}
    assert messages(spec_checks.coverage_findings(scope(fixtures, dict(placed, **swapped)))) == found
