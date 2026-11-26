"""The audit's check of a spec's Mermaid diagrams: each mermaid block of a file under the specs declares a flowchart,
read across the whole block so a block of configuration may open it, and a file outside the specs is left aside."""
import pytest

from audit_set import messages, spec_checks

pytestmark = [pytest.mark.reads("audit-mermaid-flowcharts.md", "mermaid-flowchart-after-its-configuration",
                                "mermaid-sequence-diagram")]


# @canon-spec specs/methodology/modeling-constructs.md § Diagrams
@pytest.mark.action("--check-scope")
@pytest.mark.passes
@pytest.mark.parametrize("key, path", [
    ("mermaid-flowchart-after-its-configuration", "specs/harbor.md"),
    ("mermaid-sequence-diagram", "docs/harbor.md"),
])
def test_a_flowchart_or_a_diagram_outside_the_specs_passes(fixtures, key, path):
    assert spec_checks.mermaid_flowchart_findings(path, fixtures[key]) == []


# @canon-spec specs/methodology/modeling-constructs.md § Diagrams
@pytest.mark.action("--check-scope")
@pytest.mark.reports
def test_a_mermaid_block_declaring_no_flowchart_is_reported(fixtures):
    assert messages(spec_checks.mermaid_flowchart_findings("specs/harbor.md", fixtures["mermaid-sequence-diagram"])) == [
        "a mermaid block that does not declare flowchart"]
