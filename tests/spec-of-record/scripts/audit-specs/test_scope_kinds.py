"""The audit's check of the table of what the methodology governs, where the project holds the file holding it: its
kinds are the seven the script reads, and each file or folder a row names in backticks stands."""
import pytest

from audit_set import scope, spec_checks

pytestmark = [pytest.mark.reads("audit-scope-table.md", "scope-table-of-seven-kinds", "scope-table-of-six-kinds",
                                "bakery-agent-instructions", "bakery-readme", "bakery-opening-hours")]
TABLE = "specs/methodology/scope/what-spec-of-record-governs.md"
BAKERY = {"scope-table-of-seven-kinds": TABLE, "bakery-agent-instructions": "AGENTS.md", "bakery-readme": "README.md",
          "bakery-opening-hours": "docs/opening-hours.md"}


# @canon-spec specs/methodology/scope/what-spec-of-record-governs.md § What Spec of Record Governs
@pytest.mark.action("--check-scope")
@pytest.mark.passes
@pytest.mark.parametrize("left_out", [None, "scope-table-of-seven-kinds"], ids=["table-held", "no-table-held"])
def test_a_table_of_the_seven_kinds_naming_what_stands_passes(fixtures, left_out):
    placed = {k: p for k, p in BAKERY.items() if k != left_out}
    assert spec_checks.scope_findings(scope(fixtures, placed)) == []


# @canon-spec specs/methodology/scope/what-spec-of-record-governs.md § What Spec of Record Governs
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("left_out, added, message", [
    ("scope-table-of-seven-kinds", {"scope-table-of-six-kinds": TABLE},
     "the kinds are ['Agent instructions', 'Documentation', 'Fixture files', 'Skills', 'Specs', 'Working files'], not "
     "the ones the script reads, ['Agent instructions', 'Code', 'Documentation', 'Fixture files', 'Skills', 'Specs', "
     "'Working files']"),
    ("bakery-readme", {}, "the Documentation row names README.md, which does not exist"),
], ids=["a-kind-missing", "a-home-missing"])
def test_a_table_out_of_step_with_the_kinds_or_the_files_is_reported(fixtures, left_out, added, message):
    placed = {k: p for k, p in BAKERY.items() if k != left_out} | added
    found = spec_checks.scope_findings(scope(fixtures, placed))
    assert [(path, line, m) for _, path, line, m in found] == [(TABLE, 0, message)]
