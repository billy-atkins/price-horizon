"""--free-design: a design freed of each finished or gone design it names, reassessed where its goals are agreed,
moved back where it stood approved or applying, and no design written but that one."""
import pytest

from design_script_set import DESIGN, NAME, REPORTS, WORKSTACK_READS, acted, design_documents as dd, held, workstack

pytestmark = WORKSTACK_READS


def freed(work, fixtures, monkeypatch, key):
    """-> (the project's root, every file it held before the freeing, its exit status) of a design freed."""
    root = workstack(work, fixtures, {key: DESIGN})
    before = held(root)
    return root, before, acted(monkeypatch, root, dd.free_design, DESIGN)


def others(files):
    return {path: text for path, text in files.items() if path != DESIGN}


@pytest.mark.action("--free-design")
@pytest.mark.passes
@pytest.mark.reads("design-script-workstack.md", "ferry-design-complete-naming-a-gone-design", "ferry-design-abandoned-naming-an-unfinished-design",
                   "ferry-design-drafted-naming-an-unfinished-design")
@pytest.mark.parametrize("key, said", [
    ("ferry-design-complete-naming-a-gone-design", "complete, so it is never written: each design its Depends On Designs names is its history"),
    ("ferry-design-abandoned-naming-an-unfinished-design", "abandoned, so it is never written"),
    ("ferry-design-drafted-naming-an-unfinished-design", "its Depends On Designs names no finished or gone design, so nothing is written"),
])
def test_design_finished_or_naming_none_to_free_it_of_is_left_as_it_stands(fixtures, work, monkeypatch, capsys, key, said):
    root, before, status = freed(work, fixtures, monkeypatch, key)
    assert status == 0 and said in capsys.readouterr().out and held(root) == before


@pytest.mark.action("--free-design")
@pytest.mark.passes
@pytest.mark.reads("design-script-workstack.md", "ferry-design-not-started-naming-a-complete-design", "ferry-design-entered-naming-a-gone-design")
@pytest.mark.parametrize("key, named", [("ferry-design-not-started-naming-a-complete-design", "harbor-dredged, finished"),
                                        ("ferry-design-entered-naming-a-gone-design", "tide-tables-printed, gone")])
def test_design_whose_goals_are_not_agreed_is_freed_and_takes_no_entry(fixtures, work, monkeypatch, capsys, key, named):
    root, before, status = freed(work, fixtures, monkeypatch, key)
    out, now = capsys.readouterr().out, (root / DESIGN).read_text(encoding="utf-8")
    assert status == 0 and "freed of %s; its Depends On Designs now none" % named in out
    assert "its goals are not agreed in its current major version, so no entry is appended" in out
    assert "**Depends On Designs:** none" in now and dd.log_entries(now) == dd.log_entries(fixtures[key])
    assert others(held(root)) == others(before)


@pytest.mark.action("--free-design")
@pytest.mark.passes
@pytest.mark.reads("design-script-once-mishandled.md", "ferry-design-drafted-naming-a-complete-design", "ferry-design-drafted-naming-a-gone-design")
@pytest.mark.reads("design-script-workstack.md", "ferry-design-drafted-naming-an-abandoned-design", "ferry-design-waiting-at-its-frame-naming-an-abandoned-design",
                   "ferry-design-approved-naming-a-complete-design", "ferry-design-applying-naming-a-gone-design")
@pytest.mark.parametrize("key, cause, moved", [
    ("ferry-design-drafted-naming-a-complete-design", "harbor-dredged finished", None),
    ("ferry-design-drafted-naming-an-abandoned-design", "pier-closed finished", None),
    ("ferry-design-drafted-naming-a-gone-design", "tide-tables-printed gone", None),
    ("ferry-design-waiting-at-its-frame-naming-an-abandoned-design", "pier-closed finished", None),
    ("ferry-design-approved-naming-a-complete-design", "harbor-dredged finished", "approved"),
    ("ferry-design-applying-naming-a-gone-design", "tide-tables-printed gone", "applying"),
])
def test_design_whose_goals_are_agreed_is_freed_and_reassessed(fixtures, work, monkeypatch, capsys, key, cause, moved):
    root, before, status = freed(work, fixtures, monkeypatch, key)
    out, now = capsys.readouterr().out, (root / DESIGN).read_text(encoding="utf-8")
    added = dd.log_entries(now)[len(dd.log_entries(fixtures[key])):]
    assert status == 0 and "reassessed, its goals to agree again" in out and ("moved back from %s to in-progress" % moved in out) == bool(moved)
    assert "**Depends On Designs:** none" in now and "**Version:** 2.0.0 \\\n**Status:** in-progress" in now
    assert [(kind, n) for kind, n, _ in added] == [("design-reassessment", 1)] + ([("entered", 2)] if moved else [])
    assert added[0][2] == {"Entry": "design-reassessment-1", "Timestamp": added[0][2]["Timestamp"], "Design Version": "2.0.0",
                           "Cause": "changed foundation: " + cause}
    assert not moved or added[1][2]["Reason"] == "freed"
    assert others(held(root)) == others(before)


@pytest.mark.action("--free-design")
@pytest.mark.passes
@pytest.mark.reads("design-script-once-mishandled.md", "ferry-design-drafted-naming-a-complete-design")
@pytest.mark.reads("design-script-workstack.md", "ferry-design-approved-naming-a-complete-design")
@pytest.mark.parametrize("key", ["ferry-design-drafted-naming-a-complete-design", "ferry-design-approved-naming-a-complete-design"])
def test_design_freed_holds_its_form(fixtures, work, monkeypatch, capsys, key):
    root, _, status = freed(work, fixtures, monkeypatch, key)
    assert status == 0 and acted(monkeypatch, root, dd.check_design_form, DESIGN) == 0
    assert "== check-design-form %s\n0 problems" % NAME in capsys.readouterr().out


@pytest.mark.action("--free-design")
@pytest.mark.passes
@pytest.mark.reads("design-script-once-mishandled.md", "ferry-design-drafted-naming-a-complete-design")
@pytest.mark.reads("design-script-workstack.md", "ferry-design-applying-naming-a-gone-design")
@pytest.mark.parametrize("key", ["ferry-design-drafted-naming-a-complete-design", "ferry-design-applying-naming-a-gone-design"])
def test_design_freed_takes_the_entry_of_its_framing(fixtures, work, monkeypatch, capsys, key):
    root, _, status = freed(work, fixtures, monkeypatch, key)
    assert status == 0 and acted(monkeypatch, root, dd.check_design_names, DESIGN) == 0
    assert acted(monkeypatch, root, dd.log_entry, [DESIGN, "goals-agreed"]) == 0
    assert "- **Entry:** goals-agreed-2" in capsys.readouterr().out and "**Version:** 2.0.0 \\" in (root / DESIGN).read_text(encoding="utf-8")


@pytest.mark.action("--free-design")
@pytest.mark.passes
@pytest.mark.reads("design-script-workstack.md", "ferry-design-drafted-naming-three-designs")
def test_freeing_keeps_each_unfinished_name_and_names_each_other_in_one_cause(fixtures, work, monkeypatch, capsys):
    root, _, status = freed(work, fixtures, monkeypatch, "ferry-design-drafted-naming-three-designs")
    now = (root / DESIGN).read_text(encoding="utf-8")
    assert status == 0
    assert "freed of harbor-dredged, finished; tide-tables-printed, gone; its Depends On Designs now quay-rebuilt" in capsys.readouterr().out
    assert "**Depends On Designs:** quay-rebuilt \\" in now
    assert "**Cause:** changed foundation: harbor-dredged finished; tide-tables-printed gone\n" in now


@pytest.mark.action("--check-design")
@pytest.mark.reports
@pytest.mark.reads("design-script-workstack.md", "ferry-design-approved-researched-naming-a-gone-design")
@pytest.mark.reads("design-script-reports.md", "ferry-research-report")
def test_no_research_of_an_earlier_major_version_binds_a_freed_design(fixtures, work, monkeypatch, capsys):
    research = REPORTS + "/handed-off-judgment/1.md"
    root = workstack(work, fixtures, {"ferry-design-approved-researched-naming-a-gone-design": DESIGN, "ferry-research-report": research})
    assert acted(monkeypatch, root, dd.free_design, DESIGN) == 0
    capsys.readouterr()
    assert acted(monkeypatch, root, dd.check_design, DESIGN) == 1
    out = capsys.readouterr().out
    assert ("1 assessed area rests on %s, a report the validation review does not read: no handed-off-judgment entry of the "
            "design's current major version names it" % research) in out
    assert "Read Assessment's Area covers" not in out and "is named by no Search" not in out


@pytest.mark.action("--free-design")
@pytest.mark.reports
@pytest.mark.reads("design-script-once-mishandled.md", "ferry-design-drafted-naming-a-complete-design")
@pytest.mark.parametrize("at", [".ai/plans/design-specs/archive/%s.md" % NAME, "elsewhere/%s.md" % NAME])
def test_design_in_no_plans_folder_is_not_freed(fixtures, work, monkeypatch, capsys, at):
    root = workstack(work, fixtures, {"ferry-design-drafted-naming-a-complete-design": at})
    before = held(root)
    assert acted(monkeypatch, root, dd.free_design, at) == 1
    out = capsys.readouterr().out
    assert "== free-design, not freed" in out and "it stands in no plans folder" in out and held(root) == before


@pytest.mark.action("--free-design")
@pytest.mark.reports
def test_file_that_is_not_there_is_refused(fixtures, work, monkeypatch, capsys):
    assert acted(monkeypatch, workstack(work, fixtures), dd.free_design, ".ai/plans/design-specs/no-such-file.md") == 2
    assert "no design document" in capsys.readouterr().err
