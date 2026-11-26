"""The log of a design naming a finished or gone design: no entry is appended until it is freed, a finished design
takes an entry as it stood, and the entries of a freeing are appended by the freeing alone."""
import pytest

from design_script_set import DESIGN, WORKSTACK_READS, acted, design_documents as dd, held, workstack

pytestmark = WORKSTACK_READS
FREEING = "its foundation has changed, and no entry is appended to its log until --free-design frees it"
NOT_LOGGED = "== log-entry, not logged"


@pytest.mark.action("--log-entry")
@pytest.mark.reports
@pytest.mark.reads("design-script-once-mishandled.md", "ferry-design-drafted-naming-a-complete-design")
@pytest.mark.parametrize("kind", ["entered", "goals-agreed", "plan-change", "user-edit", "another-round", "plan-approval", "apply", "self-review",
                                  "handed-off-judgment"])
def test_no_entry_of_any_kind_is_appended_before_the_freeing(fixtures, work, kind):
    root = workstack(work, fixtures, {"ferry-design-drafted-naming-a-complete-design": DESIGN})
    problems = dd.held_back(root / DESIGN, kind)
    assert len(problems) == 1 and "its Depends On Designs names harbor-dredged, finished: " + FREEING in problems[0]


@pytest.mark.action("--log-entry")
@pytest.mark.reports
@pytest.mark.reads("design-script-once-mishandled.md", "ferry-design-drafted-naming-a-gone-design")
@pytest.mark.reads("design-script-workstack.md", "ferry-design-drafted-naming-an-abandoned-design", "ferry-design-waiting-at-its-frame-naming-an-abandoned-design",
                   "ferry-design-approved-naming-a-complete-design", "ferry-design-applying-naming-a-gone-design",
                   "ferry-design-not-started-naming-a-complete-design", "ferry-design-entered-naming-a-gone-design")
@pytest.mark.parametrize("key, named", [
    ("ferry-design-drafted-naming-an-abandoned-design", "pier-closed, finished"),
    ("ferry-design-drafted-naming-a-gone-design", "tide-tables-printed, gone"),
    ("ferry-design-waiting-at-its-frame-naming-an-abandoned-design", "pier-closed, finished"),
    ("ferry-design-approved-naming-a-complete-design", "harbor-dredged, finished"),
    ("ferry-design-applying-naming-a-gone-design", "tide-tables-printed, gone"),
    ("ferry-design-not-started-naming-a-complete-design", "harbor-dredged, finished"),
    ("ferry-design-entered-naming-a-gone-design", "tide-tables-printed, gone"),
])
def test_design_in_any_unfinished_state_takes_no_entry_before_the_freeing(fixtures, work, key, named):
    root = workstack(work, fixtures, {key: DESIGN})
    assert ["its Depends On Designs names %s: " % named + FREEING in p for p in dd.held_back(root / DESIGN, "entered")] == [True]


@pytest.mark.action("--log-entry")
@pytest.mark.reports
@pytest.mark.reads("design-script-once-mishandled.md", "ferry-design-drafted-naming-a-gone-design")
def test_entry_refused_before_the_freeing_writes_nothing(fixtures, work, monkeypatch, capsys):
    root = workstack(work, fixtures, {"ferry-design-drafted-naming-a-gone-design": DESIGN})
    before = held(root)
    assert acted(monkeypatch, root, dd.log_entry, [DESIGN, "plan-change"]) == 1
    out = capsys.readouterr().out
    assert NOT_LOGGED in out and "names tide-tables-printed, gone: " + FREEING in out and held(root) == before


@pytest.mark.action("--log-entry")
@pytest.mark.passes
@pytest.mark.reads("design-script-workstack.md", "ferry-design-complete-naming-a-gone-design", "ferry-design-abandoned-naming-an-unfinished-design")
@pytest.mark.parametrize("key", ["ferry-design-complete-naming-a-gone-design", "ferry-design-abandoned-naming-an-unfinished-design"])
@pytest.mark.parametrize("kind", ["entered", "plan-change"])
def test_finished_design_has_nothing_held_back_for_the_designs_it_names(fixtures, work, key, kind):
    assert dd.held_back(workstack(work, fixtures, {key: DESIGN}) / DESIGN, kind) == []


@pytest.mark.action("--log-entry")
@pytest.mark.passes
@pytest.mark.reads("design-script-workstack.md", "ferry-design-complete-naming-a-gone-design")
def test_finished_design_takes_an_entry_as_it_stood(fixtures, work, monkeypatch, capsys):
    root = workstack(work, fixtures, {"ferry-design-complete-naming-a-gone-design": DESIGN})
    assert acted(monkeypatch, root, dd.log_entry, [DESIGN, "entered", "Reason=reopened"]) == 0
    assert "- **Entry:** entered-2" in capsys.readouterr().out
    assert "**Depends On Designs:** tide-tables-printed" in (root / DESIGN).read_text(encoding="utf-8")


@pytest.mark.action("--log-entry")
@pytest.mark.reports
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
@pytest.mark.parametrize("entry", [["design-reassessment", "Cause=changed foundation: harbor-dredged finished"], ["entered", "Reason=freed"]])
def test_entry_of_a_freeing_is_appended_by_the_freeing_alone(fixtures, work, monkeypatch, capsys, entry):
    root = workstack(work, fixtures, {"ferry-design-drafted": DESIGN})
    before = held(root)
    assert acted(monkeypatch, root, dd.log_entry, [DESIGN] + entry) == 1
    out = capsys.readouterr().out
    assert NOT_LOGGED in out and "an entry of a design freed for a changed foundation, which --free-design alone appends" in out
    assert held(root) == before
