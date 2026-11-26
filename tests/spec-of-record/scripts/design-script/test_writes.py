"""What an action writes: no design but the one it is run on, nothing in the designs naming a design that finishes,
and, of an action that checks or shows, no file at all."""
import pytest

from design_script_set import DESIGN, NAME, REPORTS, WORKSTACK_READS, acted, design_documents as dd, held, workstack

pytestmark = WORKSTACK_READS + [pytest.mark.reads("design-script-workstack.md", "design-waiting-on-the-ferry")]
PLANS = ".ai/plans/design-specs"
RESEARCH, REVIEW = REPORTS + "/handed-off-judgment/1.md", REPORTS + "/adversarial-review/1.md"
# a design naming the one acted on, in the plans folder and in its archive
WAITING = {"design-waiting-on-the-ferry": PLANS + "/waits-on-it.md"}
KEPT = {"design-waiting-on-the-ferry": PLANS + "/archive/waits-on-it.md"}


def around(work, fixtures, placed):
    """-> the root of a project holding the workstack, a design naming the design acted on in the plans folder and one
    in its archive, and each fixture placed."""
    workstack(work, fixtures, KEPT)
    return workstack(work, fixtures, {**WAITING, **placed})


def others(files, own=DESIGN):
    return {path: text for path, text in files.items() if path != own}


@pytest.mark.action("--stamp-validation", "--free-design", "--log-entry")
@pytest.mark.passes
@pytest.mark.reads("design-script-designs.md", "ferry-design-applying-edited-since-its-stamp", "ferry-design-drafted")
@pytest.mark.reads("design-script-once-mishandled.md", "ferry-design-drafted-naming-a-complete-design")
@pytest.mark.reads("design-script-reports.md", "ferry-research-report")
@pytest.mark.parametrize("key, action, value", [
    ("ferry-design-applying-edited-since-its-stamp", dd.stamp_validation, DESIGN),
    ("ferry-design-drafted-naming-a-complete-design", dd.free_design, DESIGN),
    ("ferry-design-drafted", dd.log_entry, [DESIGN, "user-edit", "Places=docs/guide.md"]),
])
def test_writing_action_writes_the_design_it_is_run_on_alone(fixtures, work, monkeypatch, key, action, value):
    root = around(work, fixtures, {key: DESIGN, "ferry-research-report": RESEARCH})
    before = held(root)
    assert acted(monkeypatch, root, action, value) == 0
    after = held(root)
    assert after[DESIGN] != before[DESIGN] and others(after) == others(before)


@pytest.mark.action("--take-up-report")
@pytest.mark.passes
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
@pytest.mark.reads("design-script-workstack.md", "ferry-review-report-handed-back")
def test_take_up_writes_the_report_alone(fixtures, work, monkeypatch):
    root = around(work, fixtures, {"ferry-design-drafted": DESIGN, "ferry-review-report-handed-back": REVIEW})
    before = held(root)
    assert acted(monkeypatch, root, dd.take_up_report, REVIEW) == 0
    after = held(root)
    assert "## Hand-back" in after[REVIEW].decode("utf-8") and others(after, REVIEW) == others(before, REVIEW)


@pytest.mark.action("--refresh-links")
@pytest.mark.passes
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
def test_refreshing_the_links_writes_no_design(fixtures, work, monkeypatch):
    root = around(work, fixtures, {"ferry-design-drafted": DESIGN})
    before = held(root, ".ai/plans")
    assert acted(monkeypatch, root, dd.refresh_links, ".") == 0
    assert held(root, ".ai/plans") == before


@pytest.mark.action("--check-design-names")
@pytest.mark.passes
@pytest.mark.reads("design-script-designs.md", "ferry-design-applying")
def test_design_naming_one_unfinished_is_blocked_by_it(fixtures, work, monkeypatch, capsys):
    root = around(work, fixtures, {"ferry-design-applying": DESIGN})
    assert acted(monkeypatch, root, dd.check_design_names, WAITING["design-waiting-on-the-ferry"]) == 0
    assert "blocked by %s, unfinished" % NAME in capsys.readouterr().out


@pytest.mark.action("--check-design-names")
@pytest.mark.reports
@pytest.mark.reads("design-script-workstack.md", "ferry-design-complete-naming-a-gone-design")
@pytest.mark.parametrize("placed, reading", [({"ferry-design-complete-naming-a-gone-design": DESIGN}, "finished"), ({}, "gone")])
def test_design_naming_one_that_finishes_reads_it_from_the_files_as_they_stand(fixtures, work, monkeypatch, capsys, placed, reading):
    root = around(work, fixtures, placed)
    assert acted(monkeypatch, root, dd.check_design_names, WAITING["design-waiting-on-the-ferry"]) == 1
    out = capsys.readouterr().out
    assert "== check-design-names waits-on-it" in out and "its Depends On Designs names %s, %s" % (NAME, reading) in out


@pytest.mark.reads("design-script-designs.md", "ferry-design-approved-researched")
@pytest.mark.reads("design-script-reports.md", "ferry-research-report")
@pytest.mark.reads("design-script-workstack.md", "ferry-review-report-handed-back")
@pytest.mark.parametrize("action, value", [
    (dd.check_cited_headings, DESIGN), (dd.check_design_form, DESIGN), (dd.check_target_kind, DESIGN), (dd.check_design, DESIGN),
    (dd.check_workstack, PLANS), (dd.show_workstack, PLANS), (dd.show_design, DESIGN), (dd.check_design_names, DESIGN),
    (dd.show_dependents, (DESIGN, "guide-says-when-the-ferry-runs")), (dd.show_validation, DESIGN), (dd.check_handed_back, REVIEW),
    (dd.check_audits, DESIGN), (dd.check_changed_files, DESIGN), (dd.check_constructs, "docs/guide.md"),
])
def test_action_that_checks_or_shows_writes_no_file(fixtures, work, monkeypatch, action, value):
    root = around(work, fixtures, {"ferry-design-approved-researched": DESIGN, "ferry-research-report": RESEARCH,
                                   "ferry-review-report-handed-back": REVIEW})
    before = held(root)
    acted(monkeypatch, root, action, value)
    assert held(root) == before
