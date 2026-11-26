"""The audit's checks of where a citation of a section leads: to a heading that stands in a file of the project, named
by its path from the root, never to an index, a record citation to the one record it names; and a skill's file
citing a section of no other skill's file."""
import pytest

from audit_set import messages, scope, spec_checks

pytestmark = [pytest.mark.reads("audit-citations.md", "bakery-ovens", "bakery-citing-its-ovens", "bakery-citing-a-flour-file",
                                "bakery-citing-ovens-from-its-folder", "bakery-citing-a-baking-section",
                                "bakery-citing-a-flour-stock-record", "index-of-a-bakery-guide", "bakery-citing-its-guide",
                                "registry-of-two-skills", "bake-bread-citing-its-reference", "bake-bread-citing-read-tides",
                                "bake-bread-proving-reference", "read-tides-skill")]
BAKERY = "docs/bakery.md"
SKILL = ".ai/skills/bake-bread/SKILL.md"
SKILLS = {"registry-of-two-skills": "specs/methodology/skills/registered-skills.md",
          "bake-bread-proving-reference": ".ai/skills/bake-bread/references/proving.md",
          "read-tides-skill": ".ai/skills/read-tides/SKILL.md"}


def bakery(fixtures, key):
    """-> the scope of a bakery's project: its ovens, its guide, and the fixture `key` as its own file."""
    return scope(fixtures, {"bakery-ovens": "docs/ovens.md", "index-of-a-bakery-guide": "specs/index.md", key: BAKERY})


# @canon-spec specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_citations_reaching_their_sections_and_records_pass(fixtures):
    held = bakery(fixtures, "bakery-citing-its-ovens")
    assert spec_checks.citation_findings(BAKERY, held.text_of[BAKERY], held) == []


# @canon-spec specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key, message", [
    ("bakery-citing-a-flour-file", "cites a file that does not exist: docs/flour.md"),
    ("bakery-citing-ovens-from-its-folder", "not a project-root path: ovens.md"),
    ("bakery-citing-a-baking-section", "no such heading path in docs/ovens.md: § Baking"),
    ("bakery-citing-a-flour-stock-record", "a record citation matches 0 records: § Open Questions [Name: Flour Stock]"),
    ("bakery-citing-its-guide", "cites an index.md, which is never a citation target"),
])
def test_a_citation_reaching_no_section_it_may_cite_is_reported(fixtures, key, message):
    held = bakery(fixtures, key)
    assert messages(spec_checks.citation_findings(BAKERY, held.text_of[BAKERY], held)) == [message]


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill
# @canon-spec specs/methodology/sourcing-and-citation/which-citations-are-allowed.md § Which Citations Are Allowed
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_a_skill_citing_its_own_files_passes(fixtures):
    held = scope(fixtures, {**SKILLS, "bake-bread-citing-its-reference": SKILL})
    assert spec_checks.skill_citation_findings(SKILL, held.text_of[SKILL], held) == []


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill
# @canon-spec specs/methodology/sourcing-and-citation/which-citations-are-allowed.md § Which Citations Are Allowed
@pytest.mark.action("--check-scope")
@pytest.mark.reports
def test_a_skill_citing_another_skills_file_is_reported(fixtures):
    held = scope(fixtures, {**SKILLS, "bake-bread-citing-read-tides": SKILL})
    assert messages(spec_checks.skill_citation_findings(SKILL, held.text_of[SKILL], held)) == [
        "cites another skill's file: .ai/skills/read-tides/SKILL.md"]
