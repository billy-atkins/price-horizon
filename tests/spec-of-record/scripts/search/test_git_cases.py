"""Git absent or failing: a search of a commit's files stops and says which case it is in, and a search of any other
target answers the same whatever version control holds."""
import os
import shutil

import pytest

HERON = ("search-heron-project.md", "heron-spec", "stack-naming-one-code-root", "heron-function", "egret-function", "design-citing-the-heron",
         "plan-citing-the-heron", "follow-ups-naming-a-heron")


@pytest.mark.action("--show-term-uses", "--show-citers")
@pytest.mark.reports
@pytest.mark.reads(*HERON)
@pytest.mark.reads("search-heron-project.md", "head-git-cannot-read")
def test_a_search_of_the_committed_files_stops_saying_why_and_every_other_target_answers(fixtures, tools, search, script, monkeypatch, work, check):
    # three copies of one small project: one committed under git, one whose `.git` folder holds a HEAD git cannot
    # read, and one with no repository at or above it below the run's folder, where the run keeps git from looking
    under_git, unreadable, under_none, empty = work / "under-git", work / "unreadable", work / "under-none", work / "no-git-on-path"
    for root in (under_git, unreadable, under_none):
        tools.a_project(root, fixtures)
    empty.mkdir()
    tools.git(under_git, "init", "-q")
    tools.git(under_git, "add", "specs", "code")
    tools.git(under_git, "commit", "-q", "-m", "first")
    tools.put(unreadable, ".git/HEAD", fixtures["head-git-cannot-read"])
    check("the three projects are told apart from their files: under git, under git, and under no version control the search reads",
          [search.version_control(r) for r in (under_git, unreadable, under_none)] == [search.GIT, search.GIT, search.NONE_READ], [search.version_control(r) for r in (under_git, unreadable, under_none)])

    def answers(root, name, **given):
        scratch = work / ("index-" + name)
        try:
            s = search.Search(root, scratch=scratch, quiet=True, **given)
        except search.CannotSearch as e:
            return str(e), scratch.exists()
        places = [str(p) for p in s.terms("heron").places] + [str(p) for p in s.citers("specs/target.md § Target").places]
        s.db.close()
        return places, True

    working = {"target": search.WORKING, "paths": [".ai/plans"]}
    want = {"current": answers(under_git, "want-current")[0], "working": answers(under_git, "want-working", **working)[0]}
    check("with git at hand, each target answers over the project under git", len(want["current"]) == 3 and len(want["working"]) == 4 and isinstance(answers(under_git, "want-committed", target=search.COMMITTED_OPERATIVE)[0], list), want)

    said, wrote = answers(unreadable, "unreadable-committed", target=search.COMMITTED_OPERATIVE)
    check("over a repository git cannot read, a search of the committed target stops, giving what it asked and git's own words, and writes nothing",
          isinstance(said, str) and "git answered with a failure" in said and "`git rev-parse --verify HEAD^{commit}`" in said and "git answered: fatal:" in said and not wrote, said)
    check("and a search of either other target answers as it does over the project under git",
          answers(unreadable, "unreadable-current")[0] == want["current"] and answers(unreadable, "unreadable-working", **working)[0] == want["working"])

    said, wrote = answers(under_none, "none-committed", target=search.COMMITTED_OPERATIVE)
    check("over a folder under no version control, a search of the committed target stops, saying the project is under no version control the search reads, and writes nothing",
          isinstance(said, str) and "under no version control the search reads" in said and not wrote, said)
    check("and a search of either other target answers as it does over the project under git",
          answers(under_none, "none-current")[0] == want["current"] and answers(under_none, "none-working", **working)[0] == want["working"])

    with monkeypatch.context() as hidden_git:
        hidden_git.setenv("PATH", str(empty))
        hidden = shutil.which("git") is None
        said, wrote = answers(under_git, "hidden-committed", target=search.COMMITTED_OPERATIVE)
        current, worked = answers(under_git, "hidden-current")[0], answers(under_git, "hidden-working", **working)[0]
        none_said = answers(under_none, "hidden-none-committed", target=search.COMMITTED_OPERATIVE)[0]
    check("with git kept from it, a search of the committed target over a project under git stops, saying git is not installed, and writes nothing",
          hidden and isinstance(said, str) and "the project is under git and git is not installed" in said and not wrote, said)
    check("and it never reads that project as under no version control, which it says of a folder under none even then",
          "no version control" not in said and isinstance(none_said, str) and "under no version control the search reads" in none_said, (said, none_said))
    check("and a search of either other target answers as it does with git at hand", current == want["current"] and worked == want["working"], (current, worked))
    # git names the commit and lists its files, and fails reading what they hold: one file's object is spoiled
    blob = tools.git(under_git, "rev-parse", "HEAD:specs/target.md").strip()
    held = under_git / ".git" / "objects" / blob[:2] / blob[2:]
    os.chmod(held, 0o666)
    held.write_bytes(b"no object git can read")
    said, wrote = answers(under_git, "spoiled-committed", target=search.COMMITTED_OPERATIVE)
    check("where git gives no content for a file the commit lists, a search of the committed target stops, giving what it asked and what git answered, and writes nothing",
          isinstance(said, str) and "git gave no content for a file the commit lists" in said and "`git cat-file --batch`" in said and "a file it calls missing" in said and not wrote, said)
    ran, printed = script(under_git, "--show-term-uses", "heron", "--target", search.COMMITTED_OPERATIVE)
    check("and the script stops with those words and no traceback", ran == 1 and "`git cat-file --batch`" in printed and "Traceback" not in printed, (ran, printed))
    check("and a search of either other target answers as it does over the project under git",
          answers(under_git, "spoiled-current")[0] == want["current"] and answers(under_git, "spoiled-working", **working)[0] == want["working"])

    ran, printed = script(under_none, "--show-term-uses", "heron", "--target", search.COMMITTED_OPERATIVE)
    check("the script stops with the same words and no usage", ran == 1 and "under no version control the search reads" in printed and "usage:" not in printed, (ran, printed))
