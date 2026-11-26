"""A name in a design's Depends On Designs, read from the plans folders as they stand: what a name reads as, what the
check of a design's names reports of it, and the workstack drawn and checked from the names."""
import pytest

from design_script_set import DESIGN, NAME, WORKSTACK_READS, acted, design_documents as dd, project, workstack

pytestmark = WORKSTACK_READS
PLANS, CODE_PLANS = ".ai/plans/design-specs", ".ai/plans/implement-specs"
CODE_DESIGN = "%s/%s.md" % (CODE_PLANS, NAME)
FINISHED_HEADING = "Finished, each one a design that may be deleted or moved at any time:"


def designs_of(root, folder=PLANS):
    return {name: dict(fields) for name, fields, _, _ in dd.read_designs(root / folder)}


@pytest.mark.parametrize("name, reading", [("quay-rebuilt", "unfinished"), ("harbor-dredged", "finished"), ("pier-closed", "finished"),
                                           ("tide-tables-printed", "gone"), ("no-such-design", "gone")])
def test_name_reads_as_the_design_of_that_name_stands_in_a_plans_folder(fixtures, work, name, reading):
    assert dd.read_name(designs_of(workstack(work, fixtures)), name) == reading


@pytest.mark.reads("design-script-workstack.md", "ferry-code-design-drafted-naming-an-unfinished-design")
@pytest.mark.parametrize("name, reading", [("implement-specs/" + NAME, "unfinished"), ("implement-specs/tide-tables-printed", "gone")])
def test_name_of_another_plans_folder_is_read_from_that_folder(fixtures, work, name, reading):
    root = workstack(work, fixtures, {"ferry-code-design-drafted-naming-an-unfinished-design": CODE_DESIGN})
    assert dd.read_name(designs_of(root), name) == reading


@pytest.mark.action("--check-design-names")
@pytest.mark.reports
@pytest.mark.reads("design-script-once-mishandled.md", "ferry-design-drafted-naming-a-complete-design", "ferry-design-drafted-naming-a-gone-design")
@pytest.mark.reads("design-script-workstack.md", "ferry-design-drafted-naming-an-abandoned-design")
@pytest.mark.parametrize("key, said", [
    ("ferry-design-drafted-naming-a-complete-design", "harbor-dredged, finished: a design of that name stands in a plans folder complete or abandoned"),
    ("ferry-design-drafted-naming-an-abandoned-design", "pier-closed, finished: a design of that name stands in a plans folder complete or abandoned"),
    ("ferry-design-drafted-naming-a-gone-design", "tide-tables-printed, gone: no design of that name stands in a plans folder"),
])
def test_name_of_a_finished_or_gone_design_is_reported(fixtures, work, monkeypatch, capsys, key, said):
    assert acted(monkeypatch, workstack(work, fixtures, {key: DESIGN}), dd.check_design_names, DESIGN) == 1
    out = capsys.readouterr().out
    assert "its Depends On Designs names %s; its foundation has changed" % said in out and "\n1 problem\n" in out


@pytest.mark.action("--check-design-names")
@pytest.mark.passes
@pytest.mark.reads("design-script-workstack.md", "ferry-design-drafted-naming-an-unfinished-design")
def test_name_of_an_unfinished_design_is_listed_as_blocking_it(fixtures, work, monkeypatch, capsys):
    root = workstack(work, fixtures, {"ferry-design-drafted-naming-an-unfinished-design": DESIGN})
    assert acted(monkeypatch, root, dd.check_design_names, DESIGN) == 0
    assert "blocked by quay-rebuilt, unfinished: it is worked no further than its agreed goals and frame\n0 problems" in capsys.readouterr().out


@pytest.mark.action("--check-design-names")
@pytest.mark.passes
@pytest.mark.reads("design-script-workstack.md", "ferry-design-complete-naming-a-gone-design", "ferry-design-abandoned-naming-an-unfinished-design")
@pytest.mark.parametrize("key", ["ferry-design-complete-naming-a-gone-design", "ferry-design-abandoned-naming-an-unfinished-design"])
def test_names_of_a_finished_design_are_its_history(fixtures, work, monkeypatch, capsys, key):
    assert acted(monkeypatch, workstack(work, fixtures, {key: DESIGN}), dd.check_design_names, DESIGN) == 0
    out = capsys.readouterr().out
    assert "so each design its Depends On Designs names is its history, and nothing follows from it\n0 problems" in out and "blocked by" not in out


@pytest.mark.action("--check-design-names")
@pytest.mark.passes
@pytest.mark.reads("design-script-designs.md", "ferry-design-agreed-undrafted", "code-design-drafted")
@pytest.mark.parametrize("key, at", [("ferry-design-agreed-undrafted", DESIGN), ("code-design-drafted", CODE_PLANS + "/code-design.md")])
def test_design_naming_no_design_passes(fixtures, work, monkeypatch, capsys, key, at):
    assert acted(monkeypatch, workstack(work, fixtures, {key: at}), dd.check_design_names, at) == 0
    out = capsys.readouterr().out
    assert "0 problems" in out and "blocked by" not in out


@pytest.mark.action("--check-design-names")
@pytest.mark.reports
@pytest.mark.reads("design-script-once-mishandled.md", "ferry-design-drafted-naming-a-complete-design")
def test_design_standing_in_an_archive_is_reported_as_in_no_plans_folder(fixtures, work, monkeypatch, capsys):
    at = PLANS + "/archive/%s.md" % NAME
    assert acted(monkeypatch, workstack(work, fixtures, {"ferry-design-drafted-naming-a-complete-design": at}), dd.check_design_names, at) == 1
    assert "it stands in no plans folder, so it is read as no design of the workstack and written by no action" in capsys.readouterr().out


@pytest.mark.action("--check-design-names")
@pytest.mark.reports
@pytest.mark.reads("design-script-workstack.md", "ferry-design-drafted-naming-three-designs")
def test_design_naming_several_has_each_finished_and_gone_name_reported(fixtures, work, monkeypatch, capsys):
    root = workstack(work, fixtures, {"ferry-design-drafted-naming-three-designs": DESIGN})
    assert acted(monkeypatch, root, dd.check_design_names, DESIGN) == 1
    out = capsys.readouterr().out
    assert all(said in out for said in ("names harbor-dredged, finished", "names tide-tables-printed, gone", "blocked by quay-rebuilt, unfinished", "\n2 problems\n"))


@pytest.mark.action("--show-workstack")
@pytest.mark.passes
@pytest.mark.reads("design-script-once-mishandled.md", "ferry-design-drafted-naming-a-complete-design", "ferry-design-drafted-naming-a-gone-design")
@pytest.mark.reads("design-script-workstack.md", "ferry-design-drafted-naming-an-unfinished-design", "ferry-design-approved-naming-an-unfinished-design",
                   "ferry-design-complete-naming-a-gone-design")
@pytest.mark.parametrize("key, drawn, listed", [
    ("ferry-design-drafted-naming-an-unfinished-design", "[in-progress, blocked by quay-rebuilt]", "frame or wait: "),
    ("ferry-design-approved-naming-an-unfinished-design", "[approved, blocked by quay-rebuilt, validated]", "move back: "),
    ("ferry-design-drafted-naming-a-complete-design", "[in-progress, waiting to be freed of harbor-dredged finished]", "free: "),
    ("ferry-design-drafted-naming-a-gone-design", "[in-progress, waiting to be freed of tide-tables-printed gone]", "free: "),
    ("ferry-design-complete-naming-a-gone-design", "[complete]", None),
])
def test_workstack_draws_each_design_by_what_its_names_read_as(fixtures, work, key, drawn, listed):
    lines = dd.check_stack(workstack(work, fixtures, {key: DESIGN}) / PLANS)[0]
    assert "  %s %s" % (NAME, drawn) in lines
    assert listed is None or any(line.startswith("  %s%s %s" % (listed, NAME, drawn)) for line in lines)


@pytest.mark.action("--show-workstack")
@pytest.mark.passes
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
def test_workstack_lists_each_finished_design_in_a_plans_folder(fixtures, work):
    lines = dd.check_stack(workstack(work, fixtures, {"ferry-design-drafted": DESIGN}) / PLANS)[0]
    assert lines[lines.index(FINISHED_HEADING) + 1:] == ["  harbor-dredged", "  pier-closed"]


@pytest.mark.action("--show-workstack")
@pytest.mark.passes
@pytest.mark.reads("design-script-workstack.md", "ferry-code-design-drafted-naming-an-unfinished-design")
@pytest.mark.parametrize("folder, drawn", [
    (PLANS, "  implement-specs/%s [in-progress, blocked by quay-rebuilt]" % NAME),
    (CODE_PLANS, "  %s [in-progress, blocked by design-specs/quay-rebuilt]" % NAME),
])
def test_workstack_names_a_design_beside_its_plans_folder_by_that_folder(fixtures, work, folder, drawn):
    root = workstack(work, fixtures, {"ferry-code-design-drafted-naming-an-unfinished-design": CODE_DESIGN})
    assert drawn in dd.check_stack(root / folder)[0]


@pytest.mark.action("--check-workstack")
@pytest.mark.reports
@pytest.mark.reads("design-script-workstack.md", "ferry-design-approved-naming-an-unfinished-design", "ferry-design-applying-naming-an-unfinished-design")
@pytest.mark.parametrize("key, status", [("ferry-design-approved-naming-an-unfinished-design", "approved"),
                                         ("ferry-design-applying-naming-an-unfinished-design", "applying")])
def test_design_past_its_framing_naming_an_unfinished_design_is_reported(fixtures, work, key, status):
    assert dd.check_stack(workstack(work, fixtures, {key: DESIGN}) / PLANS)[1] == [
        (NAME, "%s, but its Depends On Designs names quay-rebuilt, unfinished: no agent takes a blocked design past its framing, "
               "so it goes back to in-progress as its builder next works it" % status)]


@pytest.mark.action("--check-workstack")
@pytest.mark.passes
@pytest.mark.reads("design-script-once-mishandled.md", "ferry-design-drafted-naming-a-complete-design")
@pytest.mark.reads("design-script-workstack.md", "ferry-design-drafted-naming-an-unfinished-design", "ferry-design-not-started-naming-a-complete-design",
                   "ferry-design-complete-naming-a-gone-design", "ferry-design-abandoned-naming-an-unfinished-design",
                   "ferry-code-design-drafted-naming-an-unfinished-design")
@pytest.mark.parametrize("key, at", [("ferry-design-drafted-naming-an-unfinished-design", DESIGN), ("ferry-design-drafted-naming-a-complete-design", DESIGN),
                                     ("ferry-design-not-started-naming-a-complete-design", DESIGN), ("ferry-design-complete-naming-a-gone-design", DESIGN),
                                     ("ferry-design-abandoned-naming-an-unfinished-design", DESIGN),
                                     ("ferry-code-design-drafted-naming-an-unfinished-design", CODE_DESIGN)])
def test_design_short_of_its_framing_or_finished_is_no_problem_of_the_workstack(fixtures, work, key, at):
    root = workstack(work, fixtures, {key: at})
    assert dd.check_stack(root / PLANS)[1] == [] and dd.check_stack(root / CODE_PLANS)[1] == []


@pytest.mark.action("--check-workstack")
@pytest.mark.reports
@pytest.mark.reads("design-script-workstack.md", "design-first-naming-second", "design-second-naming-first", "design-first-spawned-by-second",
                   "design-second-spawned-by-first")
@pytest.mark.parametrize("first, second, problem", [
    ("design-first-naming-second", "design-second-naming-first", "Depends On Designs runs in a cycle: first -> second -> first"),
    ("design-first-spawned-by-second", "design-second-spawned-by-first", "Spawned By runs in a loop: first -> second -> first"),
])
def test_designs_naming_each_other_in_a_loop_are_reported(fixtures, work, first, second, problem):
    root = project(work, fixtures, {first: PLANS + "/first.md", second: PLANS + "/second.md"})
    assert ("first", problem) in dd.check_stack(root / PLANS)[1]


@pytest.mark.action("--show-workstack", "--check-workstack")
@pytest.mark.reports
@pytest.mark.parametrize("action", [dd.show_workstack, dd.check_workstack])
def test_folder_that_is_no_plans_folder_is_refused(fixtures, work, monkeypatch, capsys, action):
    assert acted(monkeypatch, workstack(work, fixtures), action, PLANS + "/archive") == 2
    assert "no plans folder, a skill's plans directory under .ai/plans/" in capsys.readouterr().err
