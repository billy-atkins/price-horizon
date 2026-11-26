"""The audit's check of the table of blank lines its layout check reads: where the scope holds the table's file, the
element names the layout check holds are held against the table's Input Values, and with no such file nothing is
held."""
import pytest

from audit_set import messages, scope, spec_checks

pytestmark = [pytest.mark.reads("audit-indexes.md", "harbor-moorings"),
              pytest.mark.reads("audit-blank-line-table.md", "style-specs-index", "style-methodology-index", "style-folder-index",
                                "blank-line-table-naming-each-element", "blank-line-table-naming-a-quote")]
STYLE = {"style-specs-index": "specs/index.md", "style-methodology-index": "specs/methodology/index.md",
         "style-folder-index": "specs/methodology/spec-style/index.md"}


# @canon-spec specs/methodology/spec-style/markdown.md § Blank Lines
@pytest.mark.action("--check-scope")
@pytest.mark.passes
@pytest.mark.parametrize("placed", [
    {"harbor-moorings": "docs/moorings.md"},
    {**STYLE, "blank-line-table-naming-each-element": "specs/methodology/spec-style/markdown.md"},
])
def test_a_table_naming_each_element_the_check_holds_passes(fixtures, placed):
    assert spec_checks.blank_line_table_findings(scope(fixtures, placed)) == []


# @canon-spec specs/methodology/spec-style/markdown.md § Blank Lines
@pytest.mark.action("--check-scope")
@pytest.mark.reports
def test_a_table_naming_an_element_the_check_lacks_is_reported(fixtures):
    held = scope(fixtures, {**STYLE, "blank-line-table-naming-a-quote": "specs/methodology/spec-style/markdown.md"})
    assert messages(spec_checks.blank_line_table_findings(held)) == [
        "an element the table's Input Values give that the module lacks: a quote"]
