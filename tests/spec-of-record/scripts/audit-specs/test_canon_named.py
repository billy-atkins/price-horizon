"""The audit's check that a registered skill's Python code names the canon, a file of it or a section, in a spec
annotation alone: never in another comment, after code or on a line of its own, nor in a docstring."""
import pytest

from audit_set import scope, spec_checks

pytestmark = [pytest.mark.reads("audit-skill-registry.md", "registry-of-one-skill"),
              pytest.mark.reads("audit-canon-spec-annotations.md", "loaves-spec-of-a-script-check"),
              pytest.mark.reads("audit-canon-named.md", "bread-code-naming-the-canon-in-an-annotation-alone",
                                "bread-code-naming-a-section-after-code", "bread-code-naming-a-file-in-a-docstring",
                                "bread-code-naming-a-path-in-a-comment")]
CODE = ".ai/skills/bake-bread/scripts/prove.py"
BAKERY = {"registry-of-one-skill": "specs/methodology/skills/registered-skills.md",
          "loaves-spec-of-a-script-check": "specs/methodology/loaves.md"}


# @canon-spec specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation § Citing From Code § Script Checks [Name: canon-named-only-in-an-annotation]
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_code_naming_the_canon_in_an_annotation_alone_passes(fixtures):
    placed = BAKERY | {"bread-code-naming-the-canon-in-an-annotation-alone": CODE}
    assert spec_checks.canon_named_findings(scope(fixtures, placed)) == []


# @canon-spec specs/methodology/sourcing-and-citation/writing-a-citation.md § Writing a Citation § Citing From Code § Script Checks [Name: canon-named-only-in-an-annotation]
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key, line, message", [
    ("bread-code-naming-a-section-after-code", 3,
     "names the canon outside a spec annotation: return loaf  # as § Proving has it"),
    ("bread-code-naming-a-file-in-a-docstring", 2,
     "names the canon outside a spec annotation: \"\"\"-> the loaf, proved as loaves.md has it.\"\"\""),
    ("bread-code-naming-a-path-in-a-comment", 1,
     "names the canon outside a spec annotation: # the hour comes from specs/methodology/loaves.md"),
])
def test_code_naming_the_canon_outside_an_annotation_is_reported(fixtures, key, line, message):
    found = spec_checks.canon_named_findings(scope(fixtures, BAKERY | {key: CODE}))
    assert [(path, n, m) for _, path, n, m in found] == [(CODE, line, message)]
