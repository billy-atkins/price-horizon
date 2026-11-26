"""Designs written under earlier rules: the old Depends On field, a Reliance, a design approved or drafted while it
named an unfinished design, and a log's old values, each read as it was written and written by no action now."""
import pytest

from design_script_set import DESIGN, NAME, WORKSTACK_READS, acted, design_documents as dd, held, workstack

pytestmark = WORKSTACK_READS
PLANS = ".ai/plans/design-specs"
OLD_FIELD = "ferry-design-holding-the-old-depends-on-field"
RELYING = "ferry-design-relying-on-a-complete-design"
REVIEWED = "ferry-design-reviewed-while-naming-an-unfinished-design"
RELIANCE = "its Scope holds a Reliances field, which its form does not take: a design names the designs it depends on in its Depends On Designs alone"


@pytest.mark.action("--check-workstack")
@pytest.mark.reports
@pytest.mark.reads("design-script-once-mishandled.md", OLD_FIELD)
def test_old_depends_on_field_is_reported_by_the_check_of_the_workstack(fixtures, work):
    problems = dd.check_stack(workstack(work, fixtures, {OLD_FIELD: DESIGN}) / PLANS)[1]
    assert [p for n, p in problems if n == NAME] == ["its header gives Depends On, a field its form does not take"]


@pytest.mark.action("--show-workstack")
@pytest.mark.passes
@pytest.mark.reads("design-script-once-mishandled.md", OLD_FIELD)
@pytest.mark.reads("design-script-workstack.md", RELYING)
@pytest.mark.parametrize("key", [OLD_FIELD, RELYING])
def test_old_field_or_a_reliance_draws_a_design_blocked_by_nothing(fixtures, work, key):
    assert "  %s [in-progress]" % NAME in dd.check_stack(workstack(work, fixtures, {key: DESIGN}) / PLANS)[0]


@pytest.mark.action("--check-design-names")
@pytest.mark.passes
@pytest.mark.reads("design-script-once-mishandled.md", OLD_FIELD)
@pytest.mark.reads("design-script-workstack.md", RELYING)
@pytest.mark.parametrize("key", [OLD_FIELD, RELYING])
def test_old_field_or_a_reliance_is_read_as_naming_no_design(fixtures, work, key):
    assert dd.own_names(workstack(work, fixtures, {key: DESIGN}) / DESIGN) == []


@pytest.mark.action("--log-entry")
@pytest.mark.passes
@pytest.mark.reads("design-script-once-mishandled.md", OLD_FIELD)
def test_old_field_holds_back_no_entry_of_work_past_the_frame(fixtures, work):
    assert dd.held_back(workstack(work, fixtures, {OLD_FIELD: DESIGN}) / DESIGN, "plan-change") == []


@pytest.mark.action("--check-design-form")
@pytest.mark.reports
@pytest.mark.reads("design-script-record-parts.md", "reliances-on-one-design")
@pytest.mark.parametrize("depends_on, more", [("quay-rebuilt", ""), ("none", "; its Reliances name quay-rebuilt, which its Depends On Designs does not")])
def test_reliance_is_reported_naming_each_design_the_depends_on_designs_does_not(fixtures, depends_on, more):
    assert dd.reliance_problems(fixtures["reliances-on-one-design"], depends_on, "design-specs") == [RELIANCE + more]


@pytest.mark.action("--check-design-form")
@pytest.mark.passes
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
def test_scope_holding_no_reliance_is_no_problem(fixtures):
    assert dd.reliance_problems(dd.frame_parts(fixtures["ferry-design-drafted"])["Scope"], "none", "design-specs") == []


@pytest.mark.action("--check-design-form")
@pytest.mark.reports
@pytest.mark.reads("design-script-workstack.md", RELYING)
def test_design_holding_a_reliance_is_reported_by_the_check_of_its_form(fixtures, work, monkeypatch, capsys):
    assert acted(monkeypatch, workstack(work, fixtures, {RELYING: DESIGN}), dd.check_design_form, DESIGN) == 1
    assert RELIANCE + "; its Reliances name harbor-dredged, which its Depends On Designs does not" in capsys.readouterr().out


@pytest.mark.action("--log-entry")
@pytest.mark.passes
@pytest.mark.reads("design-script-workstack.md", "ferry-design-drafted-naming-an-unfinished-design")
@pytest.mark.parametrize("reason", ["a dependency named", "sent back for a dependency"])
def test_design_moved_back_while_blocked_takes_the_entry_of_its_move(fixtures, work, monkeypatch, capsys, reason):
    root = workstack(work, fixtures, {"ferry-design-drafted-naming-an-unfinished-design": DESIGN})
    assert acted(monkeypatch, root, dd.log_entry, [DESIGN, "entered", "Reason=" + reason]) == 0
    assert "- **Entry:** entered-2" in capsys.readouterr().out


@pytest.mark.action("--check-design-form")
@pytest.mark.passes
@pytest.mark.reads("design-script-workstack.md", REVIEWED)
def test_design_drafted_and_reviewed_while_blocked_holds_its_form(fixtures, work, monkeypatch, capsys):
    assert acted(monkeypatch, workstack(work, fixtures, {REVIEWED: DESIGN}), dd.check_design_form, DESIGN) == 0
    assert "0 problems" in capsys.readouterr().out


@pytest.mark.action("--check-workstack")
@pytest.mark.passes
@pytest.mark.reads("design-script-workstack.md", REVIEWED)
def test_design_drafted_and_reviewed_while_blocked_is_no_problem_of_the_workstack(fixtures, work):
    assert dd.check_stack(workstack(work, fixtures, {REVIEWED: DESIGN}) / PLANS)[1] == []


@pytest.mark.action("--log-entry")
@pytest.mark.reports
@pytest.mark.reads("design-script-workstack.md", REVIEWED)
def test_design_drafted_and_reviewed_while_blocked_goes_no_further(fixtures, work):
    problems = dd.held_back(workstack(work, fixtures, {REVIEWED: DESIGN}) / DESIGN, "another-round")
    assert len(problems) == 1 and "another-round entry begins or continues work past the frame" in problems[0]


@pytest.mark.action("--check-design-form")
@pytest.mark.passes
@pytest.mark.reads("design-script-workstack.md", "ferry-design-holding-entry-reasons-of-earlier-rules")
def test_entry_reasons_of_earlier_rules_are_read_as_written(fixtures, work, monkeypatch, capsys):
    root = workstack(work, fixtures, {"ferry-design-holding-entry-reasons-of-earlier-rules": DESIGN})
    assert acted(monkeypatch, root, dd.check_design_form, DESIGN) == 0
    assert "0 problems" in capsys.readouterr().out


@pytest.mark.action("--log-entry")
@pytest.mark.reports
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
@pytest.mark.parametrize("reason", ["sent back to reassess", "a dependency finished", "a dependency moved back"])
def test_entry_reason_of_earlier_rules_is_appended_in_no_entry(fixtures, work, monkeypatch, capsys, reason):
    root = workstack(work, fixtures, {"ferry-design-drafted": DESIGN})
    before = held(root)
    assert acted(monkeypatch, root, dd.log_entry, [DESIGN, "entered", "Reason=" + reason]) == 1
    out = capsys.readouterr().out
    assert "== log-entry, not logged" in out and "an entered entry's Reason is not one of" in out and held(root) == before
