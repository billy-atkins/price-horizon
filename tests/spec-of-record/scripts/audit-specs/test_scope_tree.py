"""The audit's check of the scope's tree: it draws each file and folder at the top of the methodology, each folder
alone, every path it draws stands in the project, and it draws nothing the methodology's index leaves out."""
import pytest

from audit_set import messages, scope, spec_checks

SCOPE_FILE = "specs/methodology/scope/what-spec-of-record-governs.md"
pytestmark = [pytest.mark.reads("audit-scope-tree.md", "bakery-scope-drawn-whole", "bakery-scope-drawn-without-loaves",
                                "bakery-scope-drawn-into-its-folder", "bakery-scope-with-no-tree",
                                "index-of-a-bakery-methodology", "bakery-loaves")]
BAKERY = {"index-of-a-bakery-methodology": "specs/methodology/index.md", "bakery-loaves": "specs/methodology/loaves.md"}


# @canon-spec specs/methodology/scope/what-spec-of-record-governs.md § The Shape of the Scope
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_a_tree_drawing_the_methodology_as_it_stands_passes(fixtures):
    placed = dict(BAKERY, **{"bakery-scope-drawn-whole": SCOPE_FILE})
    assert spec_checks.scope_tree_findings(scope(fixtures, placed)) == []


# @canon-spec specs/methodology/scope/what-spec-of-record-governs.md § The Shape of the Scope
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("tree, left_out, message", [
    ("bakery-scope-drawn-whole", "bakery-loaves", "the tree names specs/methodology/loaves.md, which does not exist"),
    ("bakery-scope-drawn-without-loaves", None, "the tree does not name specs/methodology/loaves.md"),
    ("bakery-scope-drawn-into-its-folder", None,
     "the tree draws specs/methodology/scope/what-spec-of-record-governs.md, inside a methodology folder its own index.md lists"),
    ("bakery-scope-with-no-tree", None, "the scope's tree is missing"),
])
def test_a_tree_out_of_step_with_the_methodology_is_reported(fixtures, tree, left_out, message):
    placed = {k: p for k, p in dict(BAKERY, **{tree: SCOPE_FILE}).items() if k != left_out}
    assert messages(spec_checks.scope_tree_findings(scope(fixtures, placed))) == [message]
