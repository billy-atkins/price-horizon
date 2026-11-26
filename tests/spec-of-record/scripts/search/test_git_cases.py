"""Git absent or failing: a search of a commit's files stops and says which case it is in, and a search of any other
target answers the same whatever version control holds.

Four copies of one small project are written once in the file's folder: one committed under git, one whose
repository holds a HEAD git cannot read, one under no repository below the run's folder, where the run keeps git from
looking, and one committed under git whose spec's object has since been spoiled. A test that keeps git from the search
sets the path to an empty folder for the test alone.
"""
import pytest

from search_set import HERON, READS_HERON, ask, git, project, search

pytestmark = [READS_HERON[0], pytest.mark.reads("search-heron-project.md", "head-git-cannot-read"), pytest.mark.reads("search-commits.md", "spoiled-git-object")]
SECTION = "specs/target.md § Target"
TARGETS = {"current": {}, "working": {"target": search.WORKING, "paths": [".ai/plans"]}, "committed": {"target": search.COMMITTED_OPERATIVE}}


def committed(root):
    git(root, "init", "-q")
    git(root, "add", "specs", "code")
    git(root, "commit", "-q", "-m", "first")
    return root


@pytest.fixture
def projects(shared, fixtures):
    """-> {name: root} of the four copies of the project, and the empty folder a test keeping git from the search
    sets the path to."""
    def build():
        folder = shared.folder
        spoiled = committed(project(folder / "spoiled", fixtures, HERON))
        held = spoiled / ".git" / "objects" / git(spoiled, "rev-parse", "HEAD:specs/target.md")[:2] / git(spoiled, "rev-parse", "HEAD:specs/target.md")[2:]
        held.chmod(0o666)
        held.write_bytes(fixtures["spoiled-git-object"].encode("utf-8"))
        (folder / "no-git-on-path").mkdir()
        return {"under-git": committed(project(folder / "under-git", fixtures, HERON)),
                "unreadable": project(folder / "unreadable", fixtures, dict(HERON, **{"head-git-cannot-read": ".git/HEAD"})),
                "under-none": project(folder / "under-none", fixtures, HERON), "spoiled": spoiled, "no-git-on-path": folder / "no-git-on-path"}
    return shared.once("projects", build)


def answered(opened, root, scratch, **given):
    """-> the places a search of a target gives for a word and for the citers of a section."""
    s = opened(root, scratch=scratch, **given)
    return [str(p) for p in s.terms("heron").places] + [str(p) for p in s.citers(SECTION).places]


@pytest.fixture
def under_git(shared, projects):
    """-> {target: places} each target gives over the project under git, with git at hand."""
    return shared.once("under-git", lambda: {name: answered(shared.opened, projects["under-git"], shared.folder / ("index-" + name), **given)
                                             for name, given in TARGETS.items()})


@pytest.mark.parametrize("name, case", [("under-git", search.GIT), ("unreadable", search.GIT), ("under-none", search.NONE_READ), ("spoiled", search.GIT)])
def test_the_case_a_project_is_in_is_told_from_its_files(projects, name, case):
    assert search.version_control(projects[name]) == case


@pytest.mark.action("--show-term-uses", "--show-citers")
@pytest.mark.passes
@pytest.mark.parametrize("target, count", [("current", 3), ("working", 4), ("committed", 3)])
def test_with_git_at_hand_each_target_answers_over_the_project_under_git(under_git, target, count):
    assert len(under_git[target]) == count


@pytest.mark.action("--show-term-uses", "--show-citers")
@pytest.mark.reports
@pytest.mark.parametrize("name, hidden, said, unsaid", [
    ("unreadable", False, ["git answered with a failure", "`git rev-parse --verify HEAD^{commit}`", "git answered: fatal:"], None),
    ("under-none", False, ["under no version control the search reads"], None),
    ("under-git", True, ["the project is under git and git is not installed"], "no version control"),
    ("under-none", True, ["under no version control the search reads"], None),
    ("spoiled", False, ["git gave no content for a file the commit lists", "`git cat-file --batch`", "a file it calls missing"], None),
], ids=["git-cannot-read-the-repository", "under-no-version-control", "git-not-installed", "under-no-version-control-and-git-not-installed",
        "git-gives-no-content-for-a-file"])
def test_a_search_of_the_committed_files_stops_saying_which_case_it_is_in_and_writes_nothing(projects, opened, work, monkeypatch, name, hidden, said, unsaid):
    if hidden:
        monkeypatch.setenv("PATH", str(projects["no-git-on-path"]))
    with pytest.raises(search.CannotSearch) as stopped:
        opened(projects[name], scratch=work / "index", target=search.COMMITTED_OPERATIVE)
    assert all(words in str(stopped.value) for words in said) and not (unsaid and unsaid in str(stopped.value))
    assert not (work / "index").exists()


@pytest.mark.action("--show-term-uses", "--show-citers")
@pytest.mark.passes
@pytest.mark.parametrize("target", ["current", "working"])
@pytest.mark.parametrize("name, hidden", [("unreadable", False), ("under-none", False), ("under-git", True), ("spoiled", False)],
                         ids=["git-cannot-read-the-repository", "under-no-version-control", "git-not-installed", "git-gives-no-content-for-a-file"])
def test_a_search_of_every_other_target_answers_as_it_does_over_the_project_under_git(projects, under_git, opened, work, monkeypatch, name, hidden, target):
    if hidden:
        monkeypatch.setenv("PATH", str(projects["no-git-on-path"]))
    assert answered(opened, projects[name], work / "index", **TARGETS[target]) == under_git[target]


@pytest.mark.action("--show-term-uses")
@pytest.mark.reports
@pytest.mark.parametrize("name, said", [("under-none", "under no version control the search reads"), ("spoiled", "`git cat-file --batch`")],
                         ids=["under-no-version-control", "git-gives-no-content-for-a-file"])
def test_the_entry_script_s_main_stops_with_the_words_of_a_search_it_cannot_answer_and_no_usage(projects, capsys, name, said):
    assert ask(projects[name], "--show-term-uses", "heron", "--target", search.COMMITTED_OPERATIVE) == 1
    printed = capsys.readouterr().out
    assert said in printed and "usage:" not in printed
