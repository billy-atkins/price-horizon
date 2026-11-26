"""The audit's check of each registered skill's form: its skill file opens with front matter naming the skill by its
folder's name and describing it, holds a Workflow section, and a skill keeping scripts keeps one named for it."""
import pytest

from audit_set import scope, spec_checks

pytestmark = [pytest.mark.reads("audit-skill-form.md", "registry-of-a-bread-skill", "bread-skill-in-its-form",
                                "bread-skill-named-otherwise", "bread-skill-undescribed", "bread-skill-without-a-workflow",
                                "bread-skill-without-front-matter", "bread-script")]
REGISTRY = {"registry-of-a-bread-skill": "specs/methodology/skills/registered-skills.md"}
SKILL_FILE = ".ai/skills/bake-bread/SKILL.md"
SCRIPT = ".ai/skills/bake-bread/scripts/bake-bread.py"


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_a_skill_in_its_form_passes(fixtures):
    placed = dict(REGISTRY, **{"bread-skill-in-its-form": SKILL_FILE, "bread-script": SCRIPT})
    assert spec_checks.skill_findings(scope(fixtures, placed)) == []


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("skill, script_at, found", [
    ("bread-skill-named-otherwise", SCRIPT, [(SKILL_FILE, "front matter name is not the kebab-case directory name bake-bread")]),
    ("bread-skill-undescribed", SCRIPT, [(SKILL_FILE, "front matter has no description")]),
    ("bread-skill-without-a-workflow", SCRIPT, [(SKILL_FILE, "SKILL.md has no ## Workflow section")]),
    ("bread-skill-without-front-matter", SCRIPT, [(SKILL_FILE, "SKILL.md does not open with YAML front matter"),
                                                  (SKILL_FILE, "front matter name is not the kebab-case directory name bake-bread"),
                                                  (SKILL_FILE, "front matter has no description")]),
    ("bread-skill-in-its-form", ".ai/skills/bake-bread/scripts/knead.py",
     [(".ai/skills/bake-bread/scripts", "no entry-point script named bake-bread.py")]),
])
def test_a_skill_out_of_its_form_is_reported(fixtures, skill, script_at, found):
    placed = dict(REGISTRY, **{skill: SKILL_FILE, "bread-script": script_at})
    assert [(f[1], f[3]) for f in spec_checks.skill_findings(scope(fixtures, placed))] == found
