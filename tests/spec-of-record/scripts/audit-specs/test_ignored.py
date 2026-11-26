"""The audit's check that each working file the table of working files names is ignored by a line of the project's
ignore file naming it or a folder holding it, and un-ignored by none, a line ending in a slash naming a folder alone."""
import pytest

from audit_set import messages, scope, spec_checks

pytestmark = [pytest.mark.reads("audit-ignored.md", "bakery-working-files", "bakery-working-files-untabled", "ignore-the-bakery-folder",
                                "ignore-the-drafts-alone", "ignore-the-bakery-folder-but-its-log", "ignore-the-log-as-a-folder")]
WORKING_FILES = "specs/methodology/working-files/main.md"


# @canon-spec specs/methodology/working-files/main.md § The Working Files
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_each_working_file_ignored_passes(fixtures):
    placed = {"bakery-working-files": WORKING_FILES, "ignore-the-bakery-folder": ".gitignore"}
    assert spec_checks.ignored_findings(scope(fixtures, placed)) == []


# @canon-spec specs/methodology/working-files/main.md § The Working Files
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("table, ignore, message", [
    ("bakery-working-files", "ignore-the-drafts-alone", "a working file is not ignored: .bakery/oven-log.md"),
    ("bakery-working-files", "ignore-the-bakery-folder-but-its-log", "a working file is not ignored: .bakery/oven-log.md"),
    ("bakery-working-files", "ignore-the-log-as-a-folder", "a working file is not ignored: .bakery/oven-log.md"),
    ("bakery-working-files-untabled", "ignore-the-bakery-folder", "no table of working files to check"),
])
def test_a_working_file_left_unignored_is_reported(fixtures, table, ignore, message):
    placed = {table: WORKING_FILES, ignore: ".gitignore"}
    assert messages(spec_checks.ignored_findings(scope(fixtures, placed))) == [message]
