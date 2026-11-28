"""The project root and the files worked over: which files a search naming no project works over, where the model is
found, and how long a result's path grows."""
import re

import pytest

from search_set import HERON, PROJECT_FILES, READS_HERON, SKILL_FOLDER, git, project, run_entry, search

DEEP = 205  # the length of the path of the folder standing deep, which leaves a result's name room for some of the words asked
ASKED = "the lighthouse keeper trims the lamp wick each evening before dark and the ferry crosses the estuary at the turn of the tide " * 3


@pytest.fixture
def folders(fixtures, work):
    """-> (a project's root under git, a copy of its files version control made among its working files, and the
    root of a project under no version control)."""
    root = project(work / "main", fixtures, HERON)
    git(root, "init", "-q")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "a project made for a test")
    second = root / ".ai" / "tmp" / "worktrees" / "second"
    git(root, "worktree", "add", "-q", "--detach", str(second), "HEAD")
    return root, second, project(work / "loose", fixtures, HERON)


@READS_HERON[0]
@pytest.mark.parametrize("which, main", [(0, 0), (1, 0), (2, 2)], ids=["the-project-root", "a-copy-version-control-made", "under-no-version-control"])
def test_the_project_root_of_a_folder_is_the_one_holding_its_repository_or_the_folder_itself(folders, which, main):
    assert search.project_root_of(folders[which]) == folders[main].resolve()


def test_the_model_is_found_in_the_scratch_space_of_the_project_root_of_the_search_s_own_code():
    assert search.model_folder() == search.project_root_of(PROJECT_FILES) / search.SCRATCH / "model"


@READS_HERON[0]
@pytest.mark.parametrize("under", ["", "specs"], ids=["at-its-root", "in-a-folder-of-it"])
def test_a_search_naming_no_project_works_over_the_files_holding_the_working_directory(fixtures, work, monkeypatch, under):
    root = project(work / "heron", fixtures, HERON)
    (root / SKILL_FOLDER).mkdir(parents=True)
    monkeypatch.chdir(root / under)
    assert search.files_worked_over() == root.resolve()


def test_a_search_run_outside_every_project_works_over_the_files_its_own_code_stands_in(work, monkeypatch):
    work.mkdir(parents=True, exist_ok=True)
    monkeypatch.chdir(work)
    assert search.files_worked_over() == PROJECT_FILES


@pytest.mark.action("--show-term-uses")
@pytest.mark.passes
@READS_HERON[0]
def test_the_entry_script_run_in_a_project_writes_its_result_there_and_none_in_the_project_holding_it(fixtures, work):
    own = lambda: sorted(p.name for p in (PROJECT_FILES / search.SCRATCH / "results").glob("terms-heron-*.md"))
    before, root = own(), project(work / "heron", fixtures, HERON)
    ran, printed = run_entry(root, "--show-term-uses", "heron")
    assert ran == 0 and len(list((root / search.SCRATCH / "results").glob("terms-heron-*.md"))) == 1 and own() == before


def written(folder):
    return search.Result("terms", ASKED, [], "each form searched as a phrase", "complete", []).write(folder)


def deep(work):
    """-> a folder whose path is DEEP characters long."""
    folder = work
    while len(str(folder / "a-folder-standing-deep")) <= DEEP - 2:
        folder = folder / "a-folder-standing-deep"
    return folder / ("d" * (DEEP - len(str(folder)) - 1))


def test_a_result_written_in_a_folder_standing_deep_keeps_its_whole_path_within_the_longest_every_system_opens(work):
    path = written(deep(work) / "results")
    assert path.is_file() and len(str(path.resolve())) <= search.MAX_PATH


def test_a_result_written_in_a_folder_standing_deep_is_told_apart_by_its_two_hashes_with_the_words_asked_that_fit(work):
    assert re.fullmatch(r"terms-the-lighthouse[a-z0-9-]*-[0-9a-f]{6}-[0-9a-f]{8}\.md", written(deep(work) / "results").name)


def test_a_result_written_in_a_folder_standing_shallow_holds_the_words_asked_up_to_the_length_a_name_may_take(shared, work):
    # the file's own folder, which stands directly in the run's folder, is the shallow one
    shallow, far = written(shared.folder / "results"), written(deep(work) / "results")
    assert search.MAX_NAME - 1 <= len(shallow.name) <= search.MAX_NAME and shallow.name[-18:] == far.name[-18:]
