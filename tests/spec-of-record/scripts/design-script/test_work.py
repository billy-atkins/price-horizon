"""--check-work: the specs' and the code's script checks run over a design's work, the files a project of fixtures
under version control holds changed against its last commit, each finding new against that commit reported."""
import pytest

from design_script_set import NAME, acted, committed, design_documents as dd, project

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide"), pytest.mark.reads("design-script-designs.md", "ferry-design-applying")]
SKILLS = ("design-specs", "implement-specs")


def worked(work, fixtures, skill, changed):
    """-> the root of a project holding the guide and the design applying in a skill's plans folder, committed, then
    the fixtures changed maps written at their paths, and the design's path."""
    design = ".ai/plans/%s/%s.md" % (skill, NAME)
    root = committed(project(work, fixtures, {"island-guide": "docs/guide.md", "ferry-design-applying": design}))
    project(work, fixtures, changed)
    return root, design


@pytest.mark.action("--check-work")
@pytest.mark.passes
@pytest.mark.reads("design-script-pages-changed.md", "guide-giving-the-first-ferry")
@pytest.mark.parametrize("skill", SKILLS)
def test_work_adding_no_finding_passes(fixtures, work, monkeypatch, capsys, skill):
    root, design = worked(work, fixtures, skill, {"guide-giving-the-first-ferry": "docs/guide.md"})
    assert acted(monkeypatch, root, dd.check_work, design, plans=".ai/plans/" + skill) == 0
    assert "== check-work %s\n\n0 findings new against the last commit, over 1 changed file\n" % NAME in capsys.readouterr().out


@pytest.mark.action("--check-work")
@pytest.mark.reports
@pytest.mark.reads("design-script-pages.md", "notes-citing-the-ferry")
@pytest.mark.parametrize("skill", SKILLS)
def test_finding_the_work_added_is_reported(fixtures, work, monkeypatch, capsys, skill):
    root, design = worked(work, fixtures, skill, {"notes-citing-the-ferry": "docs/notes.md"})
    assert acted(monkeypatch, root, dd.check_work, design, plans=".ai/plans/" + skill) == 1
    out = capsys.readouterr().out
    assert "  docs/notes.md:3\n    a citation's link missing" in out and "1 finding new against the last commit, over 1 changed file" in out
