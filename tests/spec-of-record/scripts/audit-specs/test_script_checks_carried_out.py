"""The audit's check that each Script Check record is cited by a canon-spec annotation in the code of a skill its
Carried Out By names, or in the code the skills share; a kept test's annotation saying the test holds the check is
not one."""
import pytest

from audit_set import scope, spec_checks

pytestmark = [pytest.mark.reads("audit-skill-registry.md", "registry-of-one-skill", "registry-of-two-skills"),
              pytest.mark.reads("audit-canon-spec-annotations.md", "loaves-spec-of-a-script-check"),
              pytest.mark.reads("audit-script-checks-carried-out.md", "index-of-the-bakery-specs",
                                "bread-code-carrying-out-the-proving-check")]
REGISTRY = "specs/methodology/skills/registered-skills.md"
LOAVES = "specs/loaves.md"
BAKERY = {"index-of-the-bakery-specs": "specs/index.md", "loaves-spec-of-a-script-check": LOAVES}
CODE = "bread-code-carrying-out-the-proving-check"


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: script-check-carried-out]
@pytest.mark.action("--check-scope")
@pytest.mark.passes
@pytest.mark.parametrize("at", [".ai/skills/bake-bread/scripts/bake-bread.py", ".ai/skills/lib/proving.py"],
                         ids=["in-the-skill-carrying-it-out", "in-the-shared-code"])
def test_a_script_check_cited_where_it_is_carried_out_passes(fixtures, at):
    placed = BAKERY | {"registry-of-one-skill": REGISTRY, CODE: at}
    assert spec_checks.script_check_carried_out_findings(scope(fixtures, placed)) == []


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill § Script Checks [Name: script-check-carried-out]
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("placed", [
    {"registry-of-one-skill": REGISTRY},
    {"registry-of-two-skills": REGISTRY, CODE: ".ai/skills/ice-cakes/scripts/ice-cakes.py"},
    {"registry-of-one-skill": REGISTRY, CODE: "tests/spec-of-record/scripts/bake-bread/test_proving.py"},
], ids=["cited-nowhere", "cited-by-another-skill", "cited-by-a-kept-test"])
def test_a_script_check_cited_by_no_code_carrying_it_out_is_reported(fixtures, placed):
    found = spec_checks.script_check_carried_out_findings(scope(fixtures, BAKERY | placed))
    assert [(path, line, message) for _, path, line, message in found] == [
        (LOAVES, 10, "a script check no canon-spec annotation cites in the scripts of a skill carrying it out, or in "
                     "the code the skills share: loaf-proved-an-hour")]
