"""The files whose canon the design script reads each form from: those its shared code stands in, whatever
folder it is run in and whatever root it is given, or, for the shared code as a commit held it, that commit's tree;
and a form read in place from it, so a project holding no file of the canon is checked by the forms beside the script's own code."""
import pytest

from design_script_set import DESIGN, PROJECT_FILES, acted, committed, design_documents as dd, project, spec_text

pytestmark = [pytest.mark.reads("design-script-ferry.md", "island-guide")]


def test_own_files_are_those_the_shared_code_stands_in_whatever_folder_it_is_run_in(fixtures, work, monkeypatch):
    monkeypatch.chdir(project(work, fixtures, {"island-guide": "docs/guide.md"}) / "docs")
    assert spec_text.own_files() == PROJECT_FILES


def test_shared_code_a_commit_holds_reads_the_canon_of_that_commits_tree(fixtures, work, monkeypatch):
    root = committed(project(work, fixtures, {"island-guide": "docs/guide.md"}))
    monkeypatch.chdir(root)
    monkeypatch.setattr(spec_text, "__file__", "HEAD:.ai/skills/lib/spec_text.py")
    monkeypatch.setattr(spec_text.own_files, "trees", {})
    tree = spec_text.own_files()
    assert isinstance(tree, spec_text.CommitTree) and tree.commit == "HEAD"
    assert (tree / "docs/guide.md").read_text() == fixtures["island-guide"]
    assert spec_text.own_files() is tree


def test_form_is_read_in_place_from_the_script_s_own_files_in_a_project_holding_no_canon(fixtures, work, monkeypatch):
    monkeypatch.chdir(project(work, fixtures, {"island-guide": "docs/guide.md"}))
    body, path = dd.declaration(dd.LOG_HOME)
    values, counts, kinds, problems = dd.log_type()
    assert path == dd.LOG_HOME[0] and body and "apply" in kinds and problems == []


@pytest.mark.action("--check-design-form")
@pytest.mark.passes
@pytest.mark.reads("design-script-designs.md", "ferry-design-drafted")
@pytest.mark.parametrize("inside, given", [("", DESIGN), ("docs", "../" + DESIGN)])
def test_design_in_a_project_holding_no_canon_is_held_to_the_forms_beside_the_script_s_own_code(fixtures, work, monkeypatch, capsys, inside, given):
    root = project(work, fixtures, {"island-guide": "docs/guide.md", "ferry-design-drafted": DESIGN})
    assert acted(monkeypatch, root / inside, dd.check_design_form, given) == 0
    assert "0 problems" in capsys.readouterr().out
