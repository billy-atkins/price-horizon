"""The audit's check that each folder of the specifications holds an index naming each file and folder beside it,
and nothing that is not there."""
import pytest

from audit_set import messages, scope, spec_checks

pytestmark = [pytest.mark.reads("audit-indexes.md", "index-of-a-harbor-guide", "index-of-the-harbor-fees", "harbor-moorings",
                                "harbor-nightly-fees")]
GUIDE = {"index-of-a-harbor-guide": "specs/index.md", "harbor-moorings": "specs/moorings.md",
         "index-of-the-harbor-fees": "specs/fees/index.md", "harbor-nightly-fees": "specs/fees/nightly.md"}


# @canon-spec specs/methodology/spec-placement/where-a-file-goes.md § Where a File Goes
@pytest.mark.action("--check-scope")
@pytest.mark.passes
def test_folders_each_indexed_whole_pass(fixtures):
    assert spec_checks.index_findings(scope(fixtures, GUIDE)) == []


# @canon-spec specs/methodology/spec-placement/where-a-file-goes.md § Where a File Goes
@pytest.mark.action("--check-scope")
@pytest.mark.reports
@pytest.mark.parametrize("left_out, message", [
    ("index-of-the-harbor-fees", "directory has no index.md"),
    ("harbor-moorings", "a row names moorings.md, which is not here"),
])
def test_a_folder_indexed_out_of_step_with_what_it_holds_is_reported(fixtures, left_out, message):
    placed = {k: p for k, p in GUIDE.items() if k != left_out}
    assert messages(spec_checks.index_findings(scope(fixtures, placed))) == [message]
