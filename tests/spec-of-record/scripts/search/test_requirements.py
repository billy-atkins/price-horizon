"""What the search requires: checked before any search reads or writes, listed on request, and the model's files
installed by the one action that reaches the network.

No test here downloads anything. The model is installed where its files already stand, with the model's library told
to stay off the network, so it finds them and fetches nothing; the model's files stand where the search installs them
once on a machine, outside every run's folder, and are no run's output. A package is taken away from the search by
naming it as no module in the process the test runs in, or, for the entry script, by a fixture the process loads."""
import sys

import pytest

from search_set import HERON, READS_HERON, ask, project, run_entry, search

pytestmark = READS_HERON


def held_files(folder):
    return sorted(p.relative_to(folder).as_posix() for p in folder.rglob("*") if p.is_file()) if folder.is_dir() else []


@pytest.mark.action("--show-citers", "--show-lines", "--show-term-uses", "--show-pattern-matches", "--show-similar-passages", "--show-code-structure")
@pytest.mark.reports
def test_with_a_requirement_absent_a_search_stops_before_it_reads_or_writes(fixtures, work, monkeypatch):
    # every kind of search opens the search first, which checks what it requires
    root = project(work / "heron", fixtures, HERON)
    monkeypatch.setattr(search, "REQUIREMENTS", search.REQUIREMENTS + [search.Requirement("a package that is absent", "a test takes it away", "python -m pip install it", lambda root: False)])
    with pytest.raises(search.MissingRequirements) as stopped:
        search.Search(root, scratch=work / "index", quiet=True)
    assert "a package that is absent: a test takes it away" in str(stopped.value) and "to install it: python -m pip install it" in str(stopped.value)
    assert not (work / "index").exists()


@pytest.mark.action("--check-requirements")
@pytest.mark.passes
def test_check_requirements_names_each_thing_the_search_requires_as_present_and_why_it_needs_it(fixtures, work, capsys):
    root = project(work / "heron", fixtures, HERON)
    assert ask(root, "--check-requirements") == 0
    printed = capsys.readouterr().out
    assert "everything the search requires is present" in printed and printed.count("  present  ") == len(search.REQUIREMENTS) and "MISSING" not in printed
    assert all(r.name + ": " + r.why in printed for r in search.REQUIREMENTS) and not (root / search.SCRATCH).exists()


@pytest.mark.action("--check-requirements")
@pytest.mark.reports
def test_check_requirements_names_what_is_missing_with_the_command_installing_it(fixtures, work, capsys, monkeypatch):
    monkeypatch.setitem(sys.modules, "fastembed", None)
    assert ask(project(work / "heron", fixtures, HERON), "--check-requirements") == 1
    printed = capsys.readouterr().out
    assert "the search cannot run" in printed and "1 is missing" in printed and printed.count("  MISSING  ") == 1
    assert "  MISSING  fastembed: " in printed and "to install it: python -m pip install fastembed" in printed


@pytest.mark.action("--show-term-uses")
@pytest.mark.reports
@pytest.mark.reads("search-absent-requirement.md", "python-without-fastembed")
def test_the_entry_script_stops_a_search_lacking_a_requirement_with_its_report_and_no_traceback(fixtures, work):
    # the fixture is loaded by the process as its site customization, so its Python finds no fastembed
    project(work / "no-fastembed", fixtures, {"python-without-fastembed": "sitecustomize.py"})
    root = project(work / "heron", fixtures, HERON)
    ran, printed = run_entry(root, "--show-term-uses", "heron", env={"PYTHONPATH": str(work / "no-fastembed")})
    assert ran == 1 and "  MISSING  fastembed: " in printed and "Traceback" not in printed and not (root / search.SCRATCH).exists()


@pytest.mark.action("--install-model")
@pytest.mark.passes
def test_install_model_where_the_model_s_files_stand_finds_them_fetches_none_and_says_where(fixtures, work, capsys, monkeypatch):
    monkeypatch.setenv("HF_HUB_OFFLINE", "1")
    root, held = project(work / "heron", fixtures, HERON), search.model_folder()
    before = held_files(held)
    assert ask(root, "--install-model") == 0
    printed = capsys.readouterr().out
    assert "the model's files are in " + held.as_posix() in printed and "where every search of the project finds them" in printed
    assert before and held_files(held) == before and not (root / search.SCRATCH).exists()


@pytest.mark.action("--install-model")
@pytest.mark.reports
def test_install_model_is_refused_where_the_package_that_downloads_it_is_missing(fixtures, work, capsys, monkeypatch):
    monkeypatch.setitem(sys.modules, "fastembed", None)
    assert ask(project(work / "heron", fixtures, HERON), "--install-model") == 1
    printed = capsys.readouterr().out
    assert "fastembed is missing, and it downloads the model's files" in printed and "python -m pip install fastembed" in printed
