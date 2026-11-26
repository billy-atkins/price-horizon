"""--show-design: the header and the goals of a design standing in a plans folder, and nothing else of it."""
import pytest

from design_script_set import DESIGN, NAME, acted, design_documents as dd, held, project

pytestmark = [pytest.mark.reads("design-script-designs.md", "ferry-design-drafted", "ferry-design-not-started", "code-design-drafted",
                                "ferry-design-of-an-older-form", "design-holding-no-goals")]
CODE_DESIGN = ".ai/plans/implement-specs/code-design.md"
ARCHIVED = ".ai/plans/design-specs/archive/%s.md" % NAME


@pytest.mark.action("--show-design")
@pytest.mark.passes
@pytest.mark.parametrize("given", [DESIGN, NAME])
def test_header_and_goals_are_shown_and_nothing_else(fixtures, work, monkeypatch, capsys, given):
    root = project(work, fixtures, {"ferry-design-drafted": DESIGN})
    before = held(root)
    assert acted(monkeypatch, root, dd.show_design, given) == 0
    out = capsys.readouterr().out
    assert "== show-design %s [in-progress]" % NAME in out and "0 problems" in out
    assert all(w in out for w in ("Name: " + NAME, "Version: 1.0.1", "Status: in-progress", "Validated: none",
                                  "Design Goals:\n  - Name: guide-says-when-the-ferry-runs\n    Description: The guide says when the ferry runs."))
    assert not any(w in out for w in ("names the ferry without saying when it runs", "ferry-times-stated", "crossing-planned-from-the-guide", "Entry:"))
    assert held(root) == before


@pytest.mark.action("--show-design")
@pytest.mark.passes
def test_design_of_the_plans_folder_beside_is_shown_by_its_name(fixtures, work, monkeypatch, capsys):
    root = project(work, fixtures, {"ferry-design-drafted": DESIGN, "code-design-drafted": CODE_DESIGN})
    assert acted(monkeypatch, root, dd.show_design, "implement-specs/code-design") == 0
    out = capsys.readouterr().out
    assert "== show-design implement-specs/code-design [in-progress]" in out and "Name: code-design" in out


@pytest.mark.action("--show-design")
@pytest.mark.passes
def test_goals_not_yet_stated_are_shown_as_the_section_holds_them(fixtures, work, monkeypatch, capsys):
    root = project(work, fixtures, {"ferry-design-not-started": DESIGN})
    assert acted(monkeypatch, root, dd.show_design, DESIGN) == 0
    assert "Design Goals:\n  Not yet stated.\n0 problems" in capsys.readouterr().out


@pytest.mark.action("--show-design")
@pytest.mark.reports
def test_older_form_is_shown_as_far_as_it_reads(fixtures, work, monkeypatch, capsys):
    root = project(work, fixtures, {"ferry-design-of-an-older-form": DESIGN})
    before = held(root)
    assert acted(monkeypatch, root, dd.show_design, DESIGN) == 1
    out = capsys.readouterr().out
    assert all(w in out for w in ("Name: " + NAME, "Depends On: quay-rebuilt", "Design Goals:\n  The guide is to say when the ferry runs.",
                                  "Missing or not valid, so the design is old and suspect", "its header", "Kind is not ",
                                  "Design Goals has no Records field"))
    assert "names the ferry without saying when it runs" not in out and held(root) == before


@pytest.mark.action("--show-design")
@pytest.mark.reports
def test_goals_section_missing_is_named(fixtures, work, monkeypatch, capsys):
    root = project(work, fixtures, {"design-holding-no-goals": ".ai/plans/design-specs/no-goals.md"})
    assert acted(monkeypatch, root, dd.show_design, ".ai/plans/design-specs/no-goals.md") == 1
    assert "it holds no Design Goals section" in capsys.readouterr().out


@pytest.mark.action("--show-design")
@pytest.mark.reports
@pytest.mark.parametrize("at, given", [
    (ARCHIVED, ARCHIVED),
    (ARCHIVED, NAME),
    ("elsewhere/%s.md" % NAME, "elsewhere/%s.md" % NAME),
    (DESIGN, "no-such-design"),
])
def test_nothing_is_shown_outside_the_plans_folders(fixtures, work, monkeypatch, capsys, at, given):
    root = project(work, fixtures, {"ferry-design-drafted": at})
    before = held(root)
    assert acted(monkeypatch, root, dd.show_design, given) == 1
    out = capsys.readouterr().out
    assert "no design of that name stands in a plans folder, so nothing of it is shown" in out
    assert "Name:" not in out and "Design Goals" not in out and held(root) == before
