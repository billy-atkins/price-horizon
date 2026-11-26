"""The faults the design script was once found with, each held by the input it mishandled: the unit given that input
answers rightly. A fault whose input a test of another file already gives is held there: the citations of an applying
design read at the last commit, with the tests of the checkout a design is worked in; and a taken-up report's cold
parts read again, a report returned for the builder's own fault, a check cut short by a freeing refused, and a review
settled with Causes refused, with the tests of a report once taken up."""
import pytest

from design_script_set import DESIGN, NAME, REPORTS, acted, design_documents as dd, held, project

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide")]
PLANS = ".ai/plans/design-specs"
GUIDE = {"island-guide": "docs/guide.md"}


# the old Depends On field once read silently as a design's Depends On Designs
@pytest.mark.action("--check-design-form")
@pytest.mark.reports
@pytest.mark.reads("design-script-once-mishandled.md", "ferry-design-holding-the-old-depends-on-field")
def test_old_depends_on_field_is_read_under_its_own_name_and_reported(fixtures, work, monkeypatch, capsys):
    root = project(work, fixtures, {**GUIDE, "ferry-design-holding-the-old-depends-on-field": DESIGN})
    fields = dict(dd.read_design(root / DESIGN)[1])
    assert fields.get("Depends On") == "quay-rebuilt" and dd.DEPENDS_ON not in fields
    assert acted(monkeypatch, root, dd.check_design_form, DESIGN) == 1
    assert "its header gives Depends On, a field its form does not take" in capsys.readouterr().out


# a name of a design standing in no plans folder once given a second meaning, a problem of the workstack
@pytest.mark.action("--check-workstack")
@pytest.mark.passes
@pytest.mark.reads("design-script-once-mishandled.md", "ferry-design-drafted-naming-a-gone-design")
def test_name_of_a_gone_design_is_no_problem_of_the_workstack(fixtures, work, monkeypatch, capsys):
    root = project(work, fixtures, {**GUIDE, "ferry-design-drafted-naming-a-gone-design": DESIGN})
    assert acted(monkeypatch, root, dd.check_workstack, PLANS) == 0
    assert "0 problems" in capsys.readouterr().out


# a freeing once writing designs other than the one acted on, an archived one among them
@pytest.mark.action("--free-design")
@pytest.mark.passes
@pytest.mark.reads("design-script-once-mishandled.md", "ferry-design-drafted-naming-a-complete-design", "harbor-dredged-complete")
def test_freeing_writes_the_design_it_frees_alone(fixtures, work, monkeypatch, capsys):
    root = project(work, fixtures, {**GUIDE, "ferry-design-drafted-naming-a-complete-design": DESIGN,
                                    "harbor-dredged-complete": PLANS + "/harbor-dredged.md"})
    project(work, fixtures, {"harbor-dredged-complete": PLANS + "/archive/harbor-dredged.md"})
    before = held(root)
    assert acted(monkeypatch, root, dd.free_design, DESIGN) == 0
    after = held(root)
    assert after[DESIGN] != before[DESIGN]
    assert {p: b for p, b in after.items() if p != DESIGN} == {p: b for p, b in before.items() if p != DESIGN}


# the research of a design approved once read against the files, which its apply comes to change
@pytest.mark.action("--check-design")
@pytest.mark.passes
@pytest.mark.reads("design-script-designs.md", "ferry-design-approved-researched")
@pytest.mark.reads("design-script-once-mishandled.md", "ferry-research-report-reading-the-lighthouse")
def test_research_of_an_approved_design_is_not_read_again(fixtures, work, monkeypatch, capsys):
    root = project(work, fixtures, {**GUIDE, "ferry-design-approved-researched": DESIGN,
                                    "ferry-research-report-reading-the-lighthouse": REPORTS + "/handed-off-judgment/1.md"})
    assert acted(monkeypatch, root, dd.check_design, DESIGN) == 0
    assert "== check-design %s\n0 problems" % NAME in capsys.readouterr().out


# a path once judged by the place of its checkout, so no shorthand citation resolved in one kept under the working files
@pytest.mark.action("--check-cited-headings")
@pytest.mark.passes
@pytest.mark.reads("design-script-designs.md", "ferry-design-citing-the-guide-in-shorthand")
@pytest.mark.reads("design-script-pages.md", "guide-draft")
@pytest.mark.parametrize("under", ["", ".ai/tmp/worktrees/elsewhere/"])
def test_shorthand_citation_resolves_in_a_checkout_standing_anywhere(fixtures, work, monkeypatch, capsys, under):
    root = project(work, fixtures, {"island-guide": under + "docs/guide.md", "ferry-design-citing-the-guide-in-shorthand": under + DESIGN,
                                    "guide-draft": under + ".ai/tmp/design-specs/scratch/guide.md"})
    assert acted(monkeypatch, root / under, dd.check_cited_headings, DESIGN) == 0
    out = capsys.readouterr().out
    assert "2 citations, 0 broken" in out and "ok        guide.md" in out
