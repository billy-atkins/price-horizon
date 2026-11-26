"""The audit's check that a specification names no working file: a file under the specs naming the plans folder, the
follow-ups file or the tmp folder is reported, but the working files' own document, the specs' agent instructions and
a file outside the specs may name one, and a fenced block is left aside."""
import pytest

from audit_set import spec_checks

pytestmark = [pytest.mark.reads("audit-working-file-names.md", "prose-naming-no-working-file", "prose-naming-the-plans-folder",
                                "prose-naming-the-follow-ups-file", "prose-naming-the-tmp-folder")]


# @canon-spec specs/methodology/sourcing-and-citation/which-citations-are-allowed.md § Which Citations Are Allowed
@pytest.mark.action("--check-scope")
@pytest.mark.passes
@pytest.mark.parametrize("key, path", [
    ("prose-naming-no-working-file", "specs/timetable.md"),
    ("prose-naming-the-plans-folder", "specs/methodology/working-files/timetable.md"),
    ("prose-naming-the-plans-folder", "specs/AGENTS.md"),
    ("prose-naming-the-plans-folder", "docs/timetable.md"),
])
def test_a_working_file_named_where_it_may_be_passes(fixtures, key, path):
    assert spec_checks.working_file_named_findings(path, fixtures[key]) == []


# @canon-spec specs/methodology/sourcing-and-citation/which-citations-are-allowed.md § Which Citations Are Allowed
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("key, message", [
    ("prose-naming-the-plans-folder", "names a working file: .ai/plans"),
    ("prose-naming-the-follow-ups-file", "names a working file: .ai/follow-ups.md"),
    ("prose-naming-the-tmp-folder", "names a working file: .ai/tmp"),
])
def test_a_spec_naming_a_working_file_is_reported(fixtures, key, message):
    assert [(line, m) for _, line, m in spec_checks.working_file_named_findings("specs/timetable.md", fixtures[key])] == [
        (3, message)]
