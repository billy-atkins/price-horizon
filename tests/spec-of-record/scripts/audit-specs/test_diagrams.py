"""The audit's check of a diagram's form: a section of its own opening with the diagram, then its Caption and its
Sources, the sources sorted, and each source citing the diagram back."""
import pytest

from audit_set import messages, scope, spec_checks

pytestmark = [pytest.mark.reads("audit-diagrams.md", "index-of-a-ferry-guide", "crossing-drawn-from-its-sections",
                                "crossing-drawn-without-a-caption", "crossing-drawn-from-a-silent-section",
                                "crossing-drawn-from-sections-out-of-order", "crossing-drawn-after-a-sentence")]
CROSSING = "specs/crossing.md"


def ferry(fixtures, key):
    """-> the scope of a ferry's project: its guide, and the fixture `key` as its crossing."""
    return scope(fixtures, {"index-of-a-ferry-guide": "specs/index.md", key: CROSSING})


# @canon-spec specs/methodology/modeling-constructs.md § Diagrams
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_a_diagram_in_its_form_cited_back_by_its_sources_passes(fixtures):
    held = ferry(fixtures, "crossing-drawn-from-its-sections")
    assert spec_checks.diagram_form_findings(CROSSING, held.text_of[CROSSING], held) == []


# @canon-spec specs/methodology/modeling-constructs.md § Diagrams
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key, message", [
    ("crossing-drawn-without-a-caption", "a diagram not followed by its **Caption:**"),
    ("crossing-drawn-from-a-silent-section", "source does not cite the diagram back: specs/crossing.md § Sailing"),
    ("crossing-drawn-from-sections-out-of-order", "a diagram's Sources list is not sorted"),
    ("crossing-drawn-after-a-sentence", "a diagram's section holds something before the diagram"),
])
def test_a_diagram_out_of_its_form_is_reported(fixtures, key, message):
    held = ferry(fixtures, key)
    assert messages(spec_checks.diagram_form_findings(CROSSING, held.text_of[CROSSING], held)) == [message]
