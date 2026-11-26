"""One design document checked and shown: its form, the headings it cites, its Target against its Kind, the
validation review and its stamp, and the parts of a design naming a part, each action called in a project of
fixtures."""
import pytest

from design_script_set import DESIGN, NAME, REPORTS, acted, design_documents as dd, held, project

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide"),
              pytest.mark.reads("design-script-designs.md", "ferry-design-not-started", "ferry-design-drafted", "ferry-design-agreed-undrafted",
                                "ferry-design-approved", "ferry-design-approved-researched", "ferry-design-applying-edited-since-its-stamp",
                                "ferry-design-holding-a-field-out-of-its-form", "ferry-design-citing-a-heading-standing-nowhere",
                                "ferry-design-targeting-a-canon-file", "ferry-design-targeting-a-working-file", "code-design-drafted"),
              pytest.mark.reads("design-script-reports.md", "ferry-research-report"),
              pytest.mark.reads("audit-whole-project.md", "project-registry-of-one-skill")]
GOAL, OUTCOME = "guide-says-when-the-ferry-runs", "crossing-planned-from-the-guide"
RESEARCH = REPORTS + "/handed-off-judgment/1.md"
REGISTRY = "specs/methodology/skills/registered-skills.md"


def a_design(work, fixtures, key, at=DESIGN, **more):
    """-> the root of a project holding the guide and the design of the fixture given, at its place in the plans
    folder or at the place given, with the further fixtures given at their paths."""
    return project(work, fixtures, {"island-guide": "docs/guide.md", key: at, **more})


@pytest.mark.action("--check-design-form")
@pytest.mark.passes
@pytest.mark.parametrize("key", ["ferry-design-not-started", "ferry-design-agreed-undrafted", "ferry-design-drafted", "ferry-design-approved",
                                 "ferry-design-applying-edited-since-its-stamp"])
def test_form_passes_a_design_in_its_form(fixtures, work, monkeypatch, capsys, key):
    assert acted(monkeypatch, a_design(work, fixtures, key), dd.check_design_form, DESIGN) == 0
    assert "== check-design-form %s\n0 problems" % NAME in capsys.readouterr().out


@pytest.mark.action("--check-design-form")
@pytest.mark.reports
def test_form_reports_a_field_out_of_the_form(fixtures, work, monkeypatch, capsys):
    assert acted(monkeypatch, a_design(work, fixtures, "ferry-design-holding-a-field-out-of-its-form"), dd.check_design_form, DESIGN) == 1
    out = capsys.readouterr().out
    assert "its header" in out and "Reviewed By" in out


@pytest.mark.action("--check-cited-headings")
@pytest.mark.passes
def test_cited_heading_that_stands_passes(fixtures, work, monkeypatch, capsys):
    assert acted(monkeypatch, a_design(work, fixtures, "ferry-design-drafted"), dd.check_cited_headings, DESIGN) == 0
    assert "1 citation, 0 broken" in capsys.readouterr().out


@pytest.mark.action("--check-cited-headings")
@pytest.mark.reports
def test_cited_heading_that_does_not_stand_is_reported(fixtures, work, monkeypatch, capsys):
    assert acted(monkeypatch, a_design(work, fixtures, "ferry-design-citing-a-heading-standing-nowhere"), dd.check_cited_headings, DESIGN) == 1
    out = capsys.readouterr().out
    assert "BROKEN" in out and "§ The Harbor" in out and "no such heading" in out and "1 broken" in out


@pytest.mark.action("--check-cited-headings")
@pytest.mark.reports
@pytest.mark.reads("design-script-pages.md", "notes-citing-nothing")
def test_proposal_citing_nothing_is_refused(fixtures, work, monkeypatch, capsys):
    root = project(work, fixtures, {"notes-citing-nothing": "notes.md"})
    assert acted(monkeypatch, root, dd.check_cited_headings, "notes.md") == 2
    assert "no cross-file citations found" in capsys.readouterr().err


@pytest.mark.action("--check-target-kind")
@pytest.mark.passes
@pytest.mark.parametrize("key, at, plans", [
    ("ferry-design-drafted", DESIGN, None),
    ("code-design-drafted", ".ai/plans/implement-specs/code-design.md", ".ai/plans/implement-specs"),
])
def test_target_of_the_designs_kind_passes(fixtures, work, monkeypatch, capsys, key, at, plans):
    root = a_design(work, fixtures, key, at, **{"project-registry-of-one-skill": REGISTRY})
    assert acted(monkeypatch, root, dd.check_target_kind, at, plans) == 0
    assert "0 problems" in capsys.readouterr().out


@pytest.mark.action("--check-target-kind")
@pytest.mark.reports
@pytest.mark.parametrize("key, message", [
    ("ferry-design-targeting-a-canon-file", "Target names a canon-specs file in a documentation design: specs/methodology/code.md"),
    ("ferry-design-targeting-a-working-file", "Target names a working file, which no design changes: .ai/follow-ups.md"),
])
def test_target_of_another_kind_is_reported(fixtures, work, monkeypatch, capsys, key, message):
    root = a_design(work, fixtures, key, **{"project-registry-of-one-skill": REGISTRY})
    assert acted(monkeypatch, root, dd.check_target_kind, DESIGN) == 1
    assert message in capsys.readouterr().out


@pytest.mark.action("--check-design")
@pytest.mark.passes
def test_approved_design_with_its_research_passes(fixtures, work, monkeypatch, capsys):
    root = a_design(work, fixtures, "ferry-design-approved-researched", **{"ferry-research-report": RESEARCH})
    assert acted(monkeypatch, root, dd.check_design, DESIGN) == 0
    assert "== check-design %s\n0 problems" % NAME in capsys.readouterr().out


@pytest.mark.action("--check-design")
@pytest.mark.reports
@pytest.mark.parametrize("key, messages", [
    ("ferry-design-not-started", ["its design goals are not yet stated", "its design frame's Scope is not yet stated", "its steps are not yet drafted"]),
    ("ferry-design-approved-researched", ["has no Read Assessment of its Area in the reports the validation review reads"]),
])
def test_design_short_of_its_validation_is_reported(fixtures, work, monkeypatch, capsys, key, messages):
    assert acted(monkeypatch, a_design(work, fixtures, key), dd.check_design, DESIGN) == 1
    out = capsys.readouterr().out
    assert all(m in out for m in messages)


@pytest.mark.action("--show-dependents")
@pytest.mark.passes
@pytest.mark.parametrize("name, parts, said", [
    (GOAL, ["case visitor-planning-a-crossing", "principle times-stated-where-the-ferry-is-named", "frame outcome " + OUTCOME,
            "section-gives-the-first-and-last-crossing"], "4 parts name or cite " + GOAL),
    (OUTCOME, ["section-gives-the-first-and-last-crossing"], "1 part names or cites " + OUTCOME),
])
def test_dependents_of_a_part_are_listed(fixtures, work, monkeypatch, capsys, name, parts, said):
    assert acted(monkeypatch, a_design(work, fixtures, "ferry-design-drafted"), dd.show_dependents, (DESIGN, name)) == 0
    out = capsys.readouterr().out
    assert all(p in out for p in parts) and said in out


@pytest.mark.action("--show-dependents")
@pytest.mark.reports
def test_dependents_of_no_part_are_refused(fixtures, work, monkeypatch, capsys):
    assert acted(monkeypatch, a_design(work, fixtures, "ferry-design-drafted"), dd.show_dependents, (DESIGN, "no-such-part")) == 2
    assert "holds no goal, case, principle, Frame Outcome, step or step Objective named no-such-part" in capsys.readouterr().err


@pytest.mark.action("--show-validation")
@pytest.mark.passes
def test_validated_design_is_shown_validated(fixtures, work, monkeypatch, capsys):
    assert acted(monkeypatch, a_design(work, fixtures, "ferry-design-approved"), dd.show_validation, DESIGN) == 0
    assert NAME + ": validated; stamped sha256:" in capsys.readouterr().out


@pytest.mark.action("--show-validation")
@pytest.mark.reports
@pytest.mark.parametrize("key, said", [
    ("ferry-design-drafted", ": never stamped; stamped none"),
    ("ferry-design-applying-edited-since-its-stamp", ": stale; stamped sha256:"),
])
def test_stale_or_unstamped_design_is_shown_so(fixtures, work, monkeypatch, capsys, key, said):
    assert acted(monkeypatch, a_design(work, fixtures, key), dd.show_validation, DESIGN) == 0
    assert NAME + said in capsys.readouterr().out


@pytest.mark.action("--stamp-validation")
@pytest.mark.passes
def test_design_passing_validation_is_stamped(fixtures, work, monkeypatch, capsys):
    root = a_design(work, fixtures, "ferry-design-applying-edited-since-its-stamp", **{"ferry-research-report": RESEARCH})
    assert acted(monkeypatch, root, dd.stamp_validation, DESIGN) == 0
    assert "== stamp-validation\n**Validated:** " in capsys.readouterr().out
    name, fields, _, text = dd.read_design(root / DESIGN)
    assert dd.validation(text, fields)[0] == "validated"


@pytest.mark.action("--stamp-validation")
@pytest.mark.passes
def test_current_stamp_is_left_as_it_stands(fixtures, work, monkeypatch, capsys):
    root = a_design(work, fixtures, "ferry-design-approved")
    before = held(root)
    assert acted(monkeypatch, root, dd.stamp_validation, DESIGN) == 0
    assert "already validated, the stamp current" in capsys.readouterr().out and held(root) == before


@pytest.mark.action("--stamp-validation")
@pytest.mark.reports
@pytest.mark.parametrize("key, at, said", [
    ("ferry-design-agreed-undrafted", DESIGN, "its steps are not yet drafted"),
    ("ferry-design-approved", ".ai/plans/design-specs/archive/%s.md" % NAME, "it stands in no plans folder"),
])
def test_design_failing_validation_is_not_stamped(fixtures, work, monkeypatch, capsys, key, at, said):
    root = a_design(work, fixtures, key, at)
    before = held(root)
    assert acted(monkeypatch, root, dd.stamp_validation, at) == 1
    out = capsys.readouterr().out
    assert "== stamp-validation, not stamped" in out and said in out and held(root) == before
