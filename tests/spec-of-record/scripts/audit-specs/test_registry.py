"""The audit's check of the registry of skills: it stands, it names each skill it registers in backticks, it names at
least one, and each skill it names has its own skill file."""
import pytest

from audit_set import scope, spec_checks

pytestmark = [pytest.mark.reads("audit-skill-registry.md", "registry-of-one-skill", "registry-of-no-skill",
                                "registry-of-a-row-unnamed", "bread-skill-file")]
REGISTRY = "specs/methodology/skills/registered-skills.md"
SKILL = ".ai/skills/bake-bread/SKILL.md"


# @canon-spec specs/methodology/skills/registered-skills.md § Registered Skills
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_a_registry_naming_a_skill_with_its_file_passes(fixtures):
    found = spec_checks.registry_findings(scope(fixtures, {"registry-of-one-skill": REGISTRY, "bread-skill-file": SKILL}))
    assert found == []


# @canon-spec specs/methodology/skills/registered-skills.md § Registered Skills
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("placed, reported", [
    ({"registry-of-one-skill": REGISTRY}, [(0, "the registered skill bake-bread has no SKILL.md")]),
    ({"bread-skill-file": SKILL}, [(0, "the skills registry is missing, so the scope cannot be read")]),
    ({"registry-of-no-skill": REGISTRY, "bread-skill-file": SKILL},
     [(0, "the skills registry names no skill, so the scope cannot be read")]),
    ({"registry-of-a-row-unnamed": REGISTRY, "bread-skill-file": SKILL},
     [(6, "a registry row does not name a skill in backticks")]),
], ids=["skill-file-missing", "registry-missing", "no-skill-named", "row-unnamed"])
def test_a_registry_out_of_its_form_is_reported(fixtures, placed, reported):
    found = spec_checks.registry_findings(scope(fixtures, placed))
    assert [(line, message) for _, path, line, message in found] == reported
    assert {path for _, path, _, _ in found} == {REGISTRY}
