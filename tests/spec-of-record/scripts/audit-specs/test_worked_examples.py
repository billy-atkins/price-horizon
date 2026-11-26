"""The audit's check of the pointers at the worked examples: each folder or file of the examples a methodology file
names stands, and each topic's folder of the examples is named by a methodology file."""
import pytest

from audit_set import scope, spec_checks

pytestmark = [pytest.mark.reads("audit-worked-examples.md", "methodology-index-of-loaves",
                                "loaves-naming-the-sourdough-examples", "loaves-naming-sourdough-and-rye-examples",
                                "loaves-naming-a-levain-example", "sourdough-starter-example", "rye-proving-example")]
LOAVES = "specs/methodology/loaves.md"
BREAD = {"methodology-index-of-loaves": "specs/methodology/index.md",
         "sourdough-starter-example": "specs/methodology/examples/bread/sourdough/starter.md"}


# @canon-spec specs/methodology/scope/progressive-disclosure.md § Progressive Disclosure
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_examples_named_and_standing_pass(fixtures):
    placed = BREAD | {"loaves-naming-the-sourdough-examples": LOAVES}
    assert spec_checks.example_pointer_findings(scope(fixtures, placed)) == []


# @canon-spec specs/methodology/scope/progressive-disclosure.md § Progressive Disclosure
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("added, reported", [
    ({"loaves-naming-sourdough-and-rye-examples": LOAVES},
     [(LOAVES, 7, "a worked example's directory or file that does not exist: specs/methodology/examples/bread/rye")]),
    ({"loaves-naming-a-levain-example": LOAVES},
     [(LOAVES, 7, "a worked example's directory or file that does not exist: "
                  "specs/methodology/examples/bread/sourdough/levain.md")]),
    ({"loaves-naming-the-sourdough-examples": LOAVES, "rye-proving-example": "specs/methodology/examples/bread/rye/proving.md"},
     [("specs/methodology/examples/bread/rye", 0,
       "a topic of the worked examples no section of the canon names: specs/methodology/examples/bread/rye")]),
], ids=["folder-named-not-standing", "file-named-not-standing", "topic-unnamed"])
def test_an_example_named_and_not_standing_or_standing_and_not_named_is_reported(fixtures, added, reported):
    found = spec_checks.example_pointer_findings(scope(fixtures, BREAD | added))
    assert [(path, line, message) for _, path, line, message in found] == reported
