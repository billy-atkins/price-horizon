"""The audit's check of the canon-spec annotations in a registered skill's scripts: each a comment of its own in its
form, citing the methodology or the specifications' entry point, a file and a heading that stand, a part it cites
being one check's record, and each run of them on consecutive lines in plain character order."""
import pytest

from audit_set import messages, scope, spec_checks

pytestmark = [pytest.mark.reads("audit-skill-registry.md", "registry-of-one-skill"),
              pytest.mark.reads("audit-canon-spec-annotations.md", "loaves-spec-of-a-script-check",
                                "bread-script-annotated-in-form", "bread-script-annotation-after-code",
                                "bread-script-citing-an-application-spec", "bread-script-citing-an-index",
                                "bread-script-citing-cakes", "bread-script-citing-baking",
                                "bread-script-citing-a-part-of-shaping", "bread-script-citing-a-loaf-shaped-check",
                                "bread-script-annotations-shaping-first")]
SCRIPT = ".ai/skills/bake-bread/scripts/bake-bread.py"
BAKERY = {"registry-of-one-skill": "specs/methodology/skills/registered-skills.md",
          "loaves-spec-of-a-script-check": "specs/methodology/loaves.md"}


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill
# @canon-spec specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation § Citing From Code
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_annotations_in_form_citing_what_stands_pass(fixtures):
    found = spec_checks.canon_spec_findings(scope(fixtures, BAKERY | {"bread-script-annotated-in-form": SCRIPT}))
    assert found == []


# @canon-spec specs/methodology/skills/authoring-a-skill.md § Authoring a Skill
# @canon-spec specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation § Citing From Code
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key, message", [
    ("bread-script-annotation-after-code",
     "a canon-spec annotation not in its form: LOAVES = 12  # " + "@" + "canon-spec specs/methodology/loaves.md § Proving"),
    ("bread-script-citing-an-application-spec",
     "a canon-spec annotation citing neither specs/AGENTS.md nor a methodology spec: specs/bakery/loaves.md § Proving"),
    ("bread-script-citing-an-index",
     "a canon-spec annotation citing an index.md, never a citation target: specs/methodology/index.md § Loaves"),
    ("bread-script-citing-cakes", "a canon-spec annotation naming no file: specs/methodology/cakes.md"),
    ("bread-script-citing-baking", "a canon-spec annotation naming no heading: specs/methodology/loaves.md § Baking"),
    ("bread-script-citing-a-part-of-shaping",
     "a canon-spec annotation citing a part of a section that is no check's record: "
     "specs/methodology/loaves.md § Shaping [Name: by-hand]"),
    ("bread-script-citing-a-loaf-shaped-check",
     "a record citation matches 0 records: § Proving § Script Checks [Name: loaf-shaped]"),
    ("bread-script-annotations-shaping-first", "canon-spec annotations not sorted in plain character order"),
])
def test_an_annotation_out_of_its_form_or_citing_what_does_not_stand_is_reported(fixtures, key, message):
    found = spec_checks.canon_spec_findings(scope(fixtures, BAKERY | {key: SCRIPT}))
    assert messages(found) == [message]
    assert [(path, line) for _, path, line, _ in found] == [(SCRIPT, 1)]
