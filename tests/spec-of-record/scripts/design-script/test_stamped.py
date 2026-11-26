"""A check's settled report validated apart and stamped, and its entry appended only where the report holds a stamp
current with it."""
import pytest

from design_script_set import DESIGN, REPORTS, acted, design_documents as dd, held, project

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide"),
              pytest.mark.reads("design-script-designs.md", "ferry-design-drafted"),
              pytest.mark.reads("design-script-reports.md", "audit-report-finding-nothing", "audit-report-holding-a-stale-stamp",
                                "audit-report-stamped-ending-otherwise")]
AUDIT = REPORTS + "/audit-specs/1.md"
ENTRY = [DESIGN, "audit-specs", "Model=a model", "Effort=medium", "Led To=validating", "Settled Sub-scopes=documentation"]


def audited(work, fixtures, report):
    """-> the root of a project holding the guide, the design drafted and the report given as its first audit's."""
    return project(work, fixtures, {"island-guide": "docs/guide.md", "ferry-design-drafted": DESIGN, report: AUDIT})


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-stamped-only-where-its-checks-pass]
@pytest.mark.action("--stamp-settled-report")
@pytest.mark.passes
def test_report_whose_checks_pass_is_stamped(fixtures, work, monkeypatch, capsys):
    root = audited(work, fixtures, "audit-report-finding-nothing")
    assert acted(monkeypatch, root, dd.stamp_settled_report, AUDIT) == 0
    text = (root / AUDIT).read_text(encoding="utf-8")
    assert "== stamp-settled-report %s\n**Validated:** " % AUDIT in capsys.readouterr().out
    assert dd.report_stamp(text) is not None
    assert dd.stamp_problems(root, (root / DESIGN).read_text(encoding="utf-8"), "audit-specs", [], root / AUDIT) == []


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: report-stamped-only-where-its-checks-pass]
@pytest.mark.action("--stamp-settled-report")
@pytest.mark.reports
def test_report_a_check_reports_is_not_stamped_and_its_stamp_cleared(fixtures, work, monkeypatch, capsys):
    root = audited(work, fixtures, "audit-report-stamped-ending-otherwise")
    assert acted(monkeypatch, root, dd.stamp_settled_report, AUDIT) == 1
    out = capsys.readouterr().out
    assert "== stamp-settled-report, not stamped " + AUDIT in out and "its Settlement's Ending is neither `its own settling`" in out
    assert dd.report_stamp((root / AUDIT).read_text(encoding="utf-8")) is None


@pytest.mark.action("--stamp-settled-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-pages.md", "walkers-notes")
def test_file_that_is_no_report_in_a_designs_folder_is_refused(fixtures, work, monkeypatch, capsys):
    root = project(work, fixtures, {"ferry-design-drafted": DESIGN, "walkers-notes": "docs/notes.md"})
    before = held(root)
    assert acted(monkeypatch, root, dd.stamp_settled_report, "docs/notes.md") == 2
    assert "--stamp-settled-report takes a check's report at its path in a design's folder" in capsys.readouterr().err
    assert held(root) == before


# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: entry-names-a-stamped-report]
@pytest.mark.action("--log-entry")
@pytest.mark.passes
def test_entry_naming_a_report_stamped_and_unchanged_is_appended(fixtures, work, monkeypatch, capsys):
    root = audited(work, fixtures, "audit-report-finding-nothing")
    assert acted(monkeypatch, root, dd.stamp_settled_report, AUDIT) == 0
    assert acted(monkeypatch, root, dd.log_entry, ENTRY) == 0
    assert "**Entry:** audit-specs-1" in (root / DESIGN).read_text(encoding="utf-8")


# @canon-spec specs/methodology/working-files/main.md § Design Log Entry § Script Checks [Name: entry-names-a-stamped-report]
@pytest.mark.action("--log-entry")
@pytest.mark.reports
@pytest.mark.parametrize("report, said", [
    ("audit-report-finding-nothing", "holds no stamp"),
    ("audit-report-holding-a-stale-stamp", "holds a stamp no longer current with it and the files it takes in"),
])
def test_entry_naming_a_report_unstamped_or_stale_is_refused(fixtures, work, monkeypatch, capsys, report, said):
    root = audited(work, fixtures, report)
    before = held(root)
    assert acted(monkeypatch, root, dd.log_entry, ENTRY) == 1
    out = capsys.readouterr().out
    assert "== log-entry, not logged" in out and said in out and held(root) == before
