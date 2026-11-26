"""A report once taken up, and what the builder does after: no check then reads a cold part against the design or
the files, a fault in the builder's parts stays with the builder, and a check cut short by a freeing is logged."""
import pytest

from design_script_set import DESIGN, REPORTS, acted, design_documents as dd, held, project

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide")]
REVIEW = REPORTS + "/adversarial-review/1.md"
ENTRY = [DESIGN, "adversarial-review", "Model=a model", "Effort=medium", "Led To=validating"]


def round_settled(work, fixtures, design, report, **more):
    return project(work, fixtures, {"island-guide": "docs/guide.md", design: DESIGN, report: REVIEW, **more})


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-anchored-in-the-design]
@pytest.mark.action("--check-settled-report")
@pytest.mark.passes
@pytest.mark.reads("design-script-taken-up.md", "ferry-design-drafted-its-goal-renamed", "review-taken-up-its-goal-renamed-by-the-builder",
                   "ferry-design-drafted-its-objective-revised", "review-taken-up-its-finding-naming-an-objective")
@pytest.mark.parametrize("design, report", [
    ("ferry-design-drafted-its-goal-renamed", "review-taken-up-its-goal-renamed-by-the-builder"),
    ("ferry-design-drafted-its-objective-revised", "review-taken-up-its-finding-naming-an-objective"),
])
def test_finding_stands_though_the_part_it_names_is_gone_from_the_design(fixtures, work, monkeypatch, capsys, design, report):
    root = round_settled(work, fixtures, design, report)
    before = held(root)
    assert acted(monkeypatch, root, dd.check_settled_report, REVIEW) == 0
    assert "== check-settled-report %s\n0 problems" % REVIEW in capsys.readouterr().out and held(root) == before


@pytest.mark.action("--log-entry")
@pytest.mark.passes
@pytest.mark.reads("design-script-taken-up.md", "ferry-design-drafted-its-goal-renamed", "review-taken-up-its-goal-renamed-by-the-builder")
def test_entry_of_a_report_whose_finding_names_a_renamed_goal_is_appended_once_stamped(fixtures, work, monkeypatch, capsys):
    root = round_settled(work, fixtures, "ferry-design-drafted-its-goal-renamed", "review-taken-up-its-goal-renamed-by-the-builder")
    assert acted(monkeypatch, root, dd.stamp_settled_report, REVIEW) == 0
    assert acted(monkeypatch, root, dd.log_entry, ENTRY) == 0
    assert "- **Entry:** adversarial-review-1" in capsys.readouterr().out


# @canon-spec specs/methodology/working-files/main.md § A Check's Report § Script Checks [Name: findings-settled-once]
@pytest.mark.action("--check-settled-report", "--stamp-settled-report")
@pytest.mark.reports
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
@pytest.mark.reads("design-script-taken-up.md", "review-taken-up-settling-another-finding")
@pytest.mark.parametrize("action, heading", [
    (dd.check_settled_report, "== check-settled-report"),
    (dd.stamp_settled_report, "== stamp-settled-report, not stamped"),
])
def test_builders_fault_stays_with_the_builder(fixtures, work, monkeypatch, capsys, action, heading):
    root = round_settled(work, fixtures, "ferry-design-drafted", "review-taken-up-settling-another-finding")
    before = held(root)
    assert acted(monkeypatch, root, action, REVIEW) == 1
    out = capsys.readouterr().out
    assert heading in out and "Finding reviewer-1-last-crossing-in-winter is settled by 0 Settlements, not exactly one" in out
    assert "goes back to its cold agent" not in out and held(root) == before


@pytest.mark.action("--log-entry")
@pytest.mark.passes
@pytest.mark.reads("design-script-taken-up.md", "ferry-design-freed-of-a-complete-design", "review-taken-up-cut-short-by-a-freeing")
@pytest.mark.reads("design-script-once-mishandled.md", "harbor-dredged-complete")
def test_check_cut_short_by_a_freeing_is_logged_at_the_version_its_report_read(fixtures, work, monkeypatch, capsys):
    root = round_settled(work, fixtures, "ferry-design-freed-of-a-complete-design", "review-taken-up-cut-short-by-a-freeing",
                         **{"harbor-dredged-complete": ".ai/plans/design-specs/harbor-dredged.md"})
    assert acted(monkeypatch, root, dd.check_settled_report, REVIEW) == 0
    assert acted(monkeypatch, root, dd.stamp_settled_report, REVIEW) == 0
    assert acted(monkeypatch, root, dd.log_entry, ENTRY) == 0
    assert "**Design Version:** 1.0.1 \\\n    **Model:**" in capsys.readouterr().out
    assert "**Version:** 2.0.0 \\" in (root / DESIGN).read_text(encoding="utf-8")
    assert acted(monkeypatch, root, dd.check_design_form, DESIGN) == 0
