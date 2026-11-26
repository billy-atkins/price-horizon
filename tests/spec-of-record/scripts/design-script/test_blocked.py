"""The log of a design naming an unfinished design: an entry that begins or continues work past the frame is refused,
and each other entry is appended."""
import pytest

from design_script_set import DESIGN, NAME, REPORTS, WORKSTACK_READS, acted, design_documents as dd, held, workstack

pytestmark = WORKSTACK_READS + [pytest.mark.reads("design-script-workstack.md", "ferry-design-drafted-naming-an-unfinished-design")]
BLOCKED = ("entry begins or continues work past the frame, and its Depends On Designs names %s, unfinished: a blocked design is "
           "worked no further than its agreed goals and frame")
DRAFTED = "ferry-design-drafted-naming-an-unfinished-design"


@pytest.mark.action("--log-entry")
@pytest.mark.reports
@pytest.mark.parametrize("kind", ["plan-change", "design-refactor-refine", "self-review", "another-round", "plan-approval", "step-back", "apply"])
def test_entry_of_work_past_the_frame_is_held_back_from_a_blocked_design(fixtures, work, kind):
    problems = dd.held_back(workstack(work, fixtures, {DRAFTED: DESIGN}) / DESIGN, kind)
    assert len(problems) == 1 and (" %s " % kind + BLOCKED % "quay-rebuilt") in problems[0]


@pytest.mark.action("--log-entry")
@pytest.mark.reports
@pytest.mark.reads("design-script-workstack.md", "ferry-design-approved-naming-an-unfinished-design", "ferry-design-applying-naming-an-unfinished-design",
                   "ferry-code-design-drafted-naming-an-unfinished-design")
@pytest.mark.parametrize("key, at, named", [
    ("ferry-design-approved-naming-an-unfinished-design", DESIGN, "quay-rebuilt"),
    ("ferry-design-applying-naming-an-unfinished-design", DESIGN, "quay-rebuilt"),
    ("ferry-code-design-drafted-naming-an-unfinished-design", ".ai/plans/implement-specs/%s.md" % NAME, "design-specs/quay-rebuilt"),
])
def test_entry_of_work_past_the_frame_is_held_back_from_any_design_naming_an_unfinished_one(fixtures, work, key, at, named):
    problems = dd.held_back(workstack(work, fixtures, {key: at}) / at, "plan-change")
    assert len(problems) == 1 and BLOCKED % named in problems[0]


@pytest.mark.action("--log-entry")
@pytest.mark.reports
def test_entry_of_work_past_the_frame_refused_writes_nothing(fixtures, work, monkeypatch, capsys):
    root = workstack(work, fixtures, {DRAFTED: DESIGN})
    before = held(root)
    assert acted(monkeypatch, root, dd.log_entry, [DESIGN, "another-round"]) == 1
    out = capsys.readouterr().out
    assert "== log-entry, not logged" in out and "another-round " + BLOCKED % "quay-rebuilt" in out and held(root) == before


@pytest.mark.action("--log-entry")
@pytest.mark.passes
@pytest.mark.parametrize("kind", ["entered", "goals-agreed", "steer", "user-edit", "passes-choice", "direct-edit", "audit-bypass", "handed-off-judgment",
                                  "adversarial-review", "post-apply-review", "audit-specs", "verify-spec-implementation", "design-reassessment"])
def test_entry_of_no_work_past_the_frame_is_held_back_from_no_blocked_design(fixtures, work, kind):
    assert dd.held_back(workstack(work, fixtures, {DRAFTED: DESIGN}) / DESIGN, kind) == []


@pytest.mark.action("--log-entry")
@pytest.mark.passes
def test_entry_of_no_work_past_the_frame_is_appended_to_a_blocked_design(fixtures, work, monkeypatch, capsys):
    root = workstack(work, fixtures, {DRAFTED: DESIGN})
    assert acted(monkeypatch, root, dd.log_entry, [DESIGN, "user-edit", "Places=docs/guide.md"]) == 0
    assert "- **Entry:** user-edit-1" in capsys.readouterr().out
    assert "**Depends On Designs:** quay-rebuilt" in (root / DESIGN).read_text(encoding="utf-8")


@pytest.mark.action("--log-entry")
@pytest.mark.passes
@pytest.mark.reads("design-script-reports.md", "audit-report-finding-nothing")
def test_entry_of_a_check_is_appended_to_a_blocked_design_once_its_report_is_stamped(fixtures, work, monkeypatch, capsys):
    audit = REPORTS + "/audit-specs/1.md"
    root = workstack(work, fixtures, {DRAFTED: DESIGN, "audit-report-finding-nothing": audit})
    assert acted(monkeypatch, root, dd.stamp_settled_report, audit) == 0
    entry = [DESIGN, "audit-specs", "Model=a model", "Effort=medium", "Led To=validating", "Settled Sub-scopes=documentation"]
    assert acted(monkeypatch, root, dd.log_entry, entry) == 0
    assert "- **Entry:** audit-specs-1" in capsys.readouterr().out
